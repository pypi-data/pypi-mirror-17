"""
AngleConstraints contains classes for all constraints related angles between atoms.

.. inheritance-diagram:: fullrmc.Constraints.AngleConstraints
    :parts: 1
"""

# standard libraries imports
import itertools
import copy

# external libraries imports
import numpy as np

# fullrmc imports
from fullrmc.Globals import INT_TYPE, FLOAT_TYPE, PI, PRECISION, FLOAT_PLUS_INFINITY, LOGGER
from fullrmc.Core.Collection import is_number, is_integer, get_path
from fullrmc.Core.Constraint import Constraint, SingularConstraint, RigidConstraint
from fullrmc.Core.angles import full_angles_coords


class BondsAngleConstraint(RigidConstraint, SingularConstraint):
    """
    Controls the angle defined between 3 defined 'bonded' atoms.
    
    .. raw:: html

        <iframe width="560" height="315" 
        src="https://www.youtube.com/embed/ezBbbO9IVig" 
        frameborder="0" allowfullscreen>
        </iframe>
        
    
    :Parameters:
        #. anglesMap (list): The angles map definition.
           Every item must be a list of five items.
           
            #. First item: The central atom index.
            #. Second item: The index of the left atom forming the angle (interchangeable with the right atom).
            #. Third item: The index of the right atom forming the angle (interchangeable with the left atom).
            #. Fourth item: The minimum lower limit or the minimum angle allowed 
               in degrees which later will be converted to rad.
            #. Fifth item: The maximum upper limit or the maximum angle allowed 
               in degrees which later will be converted to rad.
        #. rejectProbability (Number): rejecting probability of all steps where standardError increases. 
           It must be between 0 and 1 where 1 means rejecting all steps where standardError increases
           and 0 means accepting all steps regardless whether standardError increases or not.
    
    .. code-block:: python
    
        ## Methane (CH4) molecule sketch
        ## 
        ##              H4
        ##              |
        ##              |
        ##           _- C -_
        ##        H1-  /    -_
        ##            /       H3
        ##           H2
        
        # import fullrmc modules
        from fullrmc.Engine import Engine
        from fullrmc.Constraints.AngleConstraints import BondsAngleConstraint
        
        # create engine 
        ENGINE = Engine(path='my_engine.rmc')
        
        # set pdb file
        ENGINE.set_pdb('system.pdb')
        
        # create and add constraint
        BAC = BondsAngleConstraint()
        ENGINE.add_constraints(BAC)
        
        # define intra-molecular angles 
        BAC.create_angles_by_definition( anglesDefinition={"CH4": [ ('C','H1','H2', 100, 120),
                                                                    ('C','H2','H3', 100, 120),
                                                                    ('C','H3','H4', 100, 120),
                                                                    ('C','H4','H1', 100, 120) ]} )
                                                                          
            
    """
    def __init__(self, anglesMap=None, rejectProbability=1):
        # initialize constraint
        RigidConstraint.__init__(self, rejectProbability=rejectProbability)
        # set bonds map
        self.set_angles(anglesMap)
        # set computation cost
        self.set_computation_cost(2.0)
        # create dump flag
        self.__dumpAngles = True
        # set frame data
        FRAME_DATA = [d for d in self.FRAME_DATA]
        FRAME_DATA.extend(['_BondsAngleConstraint__anglesMap',
                           '_BondsAngleConstraint__angles',
                           '_BondsAngleConstraint__atomsLUAD'] )
        RUNTIME_DATA = [d for d in self.RUNTIME_DATA]
        RUNTIME_DATA.extend( [] )
        object.__setattr__(self, 'FRAME_DATA',  tuple(FRAME_DATA)   )
        object.__setattr__(self, 'RUNTIME_DATA',tuple(RUNTIME_DATA) )
        
    @property
    def anglesMap(self):
        """ Get angles map."""
        return self.__anglesMap
    
    @property
    def angles(self):
        """ Get angles dictionary."""
        return self.__angles
    
    @property
    def atomsLUAD(self):
        """ Get look up angles dictionary, connecting every atom's index to a central atom angles definition of angles attribute."""
        return self.__atomsLUAD
        
    @property
    def standardError(self):
        """ Get constraint's current standard error."""
        if self.data is None:
            return None
        else: 
            return self.compute_standard_error(data = self.data)
            
    def listen(self, message, argument=None):
        """   
        Listens to any message sent from the Broadcaster.
        
        :Parameters:
            #. message (object): Any python object to send to constraint's listen method.
            #. argument (object): Any type of argument to pass to the listeners.
        """
        if message in("engine set","update boundary conditions",):
            # set angles and reset constraint
            self.set_angles( self.__anglesMap )
        
    def should_step_get_rejected(self, standardError):
        """
        Overloads 'RigidConstraint' should_step_get_rejected method.
        It computes whether to accept or reject a move based on before and after move calculation and not standardError.
        If any of activeAtomsDataBeforeMove or activeAtomsDataAfterMove is None an Exception will get raised.
        
        :Parameters:
            #. standardError (number): not used in this case
        
        :Return:
            #. result (boolean): True to reject step, False to accept
        """
        if self.activeAtomsDataBeforeMove is None or self.activeAtomsDataAfterMove is None:
            raise Exception(LOGGER.error("must compute data before and after group move"))
        reject = False
        for index in self.activeAtomsDataBeforeMove.keys():
            before = self.activeAtomsDataBeforeMove[index]["reducedAngles"]
            after  = self.activeAtomsDataAfterMove[index]["reducedAngles"]
            if np.any((after-before)>PRECISION):
                reject = True
                break
        return reject
        
    def set_angles(self, anglesMap):
        """ 
        Sets the angles dictionary by parsing the anglesMap list.
        
        :Parameters:
            #. anglesMap (list): The angles map definition.
               Every item must be a list of five items.
               
               #. First item: The central atom index.
               #. Second item: The index of the left atom forming the angle (interchangeable with the right atom).
               #. Third item: The index of the right atom forming the angle (interchangeable with the left atom).
               #. Fourth item: The minimum lower limit or the minimum angle allowed 
                  in degrees which later will be converted to rad.
               #. Fifth item: The maximum upper limit or the maximum angle allowed 
                  in degrees which later will be converted to rad.
        """
        map = []
        if self.engine is not None:
            if anglesMap is not None:
                assert isinstance(anglesMap, (list, set, tuple)), LOGGER.error("anglesMap must be None or a list")
                for angle in anglesMap:
                    assert isinstance(angle, (list, set, tuple)), LOGGER.error("anglesMap items must be lists")
                    angle = list(angle)
                    assert len(angle)==5, LOGGER.error("anglesMap items must be lists of 5 items each")
                    centralIdx, leftIdx, rightIdx, lower, upper = angle
                    assert is_integer(centralIdx), LOGGER.error("anglesMap items lists of first item must be an integer")
                    centralIdx = INT_TYPE(centralIdx)
                    assert is_integer(leftIdx), LOGGER.error("anglesMap items lists of second item must be an integer")
                    leftIdx = INT_TYPE(leftIdx)
                    assert is_integer(rightIdx), LOGGER.error("anglesMap items lists of third item must be an integer")
                    rightIdx = INT_TYPE(rightIdx)
                    assert centralIdx>=0, LOGGER.error("anglesMap items lists first item must be positive")
                    assert leftIdx>=0, LOGGER.error("anglesMap items lists second item must be positive")
                    assert rightIdx>=0, LOGGER.error("anglesMap items lists third item must be positive")
                    assert centralIdx!=leftIdx, LOGGER.error("bondsMap items lists first and second items can't be the same")
                    assert centralIdx!=rightIdx, LOGGER.error("bondsMap items lists first and third items can't be the same")
                    assert leftIdx!=rightIdx, LOGGER.error("bondsMap items lists second and third items can't be the same")
                    map.append((centralIdx, leftIdx, rightIdx, lower, upper))  
        # reset anglesMap definition where angles are in degrees
        self.__anglesMap = []
        # create bonds list of indexes arrays
        self.__angles    = {}
        self.__atomsLUAD = {}
        if self.engine is not None:
            # parse anglesMap
            self.__dumpAngles = False
            try:
                for angle in map:
                    self.add_angle(angle)
            except Exception as e:
                self.__dumpAngles = True
                raise LOGGER.error(e)
            self.__dumpAngles = True
            # finalize angles
            for idx in self.engine.pdb.xindexes:
                angles = self.__angles.get(idx, {"leftIndexes":[],"rightIndexes":[],"lower":[],"upper":[]} )
                self.__angles[INT_TYPE(idx)] =  {"leftIndexes": np.array(angles["leftIndexes"], dtype = INT_TYPE), 
                                                 "rightIndexes": np.array(angles["rightIndexes"], dtype = INT_TYPE),
                                                 "lower"  : np.array(angles["lower"]  , dtype = FLOAT_TYPE),
                                                 "upper"  : np.array(angles["upper"]  , dtype = FLOAT_TYPE) }
                lut = self.__atomsLUAD.get(idx, [] )
                self.__atomsLUAD[INT_TYPE(idx)] = sorted(set(lut))
        # dump to repository
        self._dump_to_repository({'_BondsAngleConstraint__anglesMap' :self.__anglesMap,
                                  '_BondsAngleConstraint__angles'    :self.__angles,
                                  '_BondsAngleConstraint__anglesLUAD':self.__atomsLUAD})
        # reset constraint
        self.reset_constraint()
    
    def add_angle(self, angle):
        """
        Add a single angle to the list of constraint angles.
        
        :Parameters:
            #. angle (list): The bond list of five items.\n
               #. First item: The central atom index.
               #. Second item: The index of the left atom forming the angle (interchangeable with the right atom).
               #. Third item: The index of the right atom forming the angle (interchangeable with the left atom).
               #. Fourth item: The minimum lower limit or the minimum angle allowed 
                  in degrees which later will be converted to rad.
               #. Fifth item: The maximum upper limit or the maximum angle allowed 
                  in degrees which later will be converted to rad.
        """
        centralIdx, leftIdx, rightIdx, lower, upper = angle
        assert centralIdx<len(self.engine.pdb), LOGGER.error("angle atom index must be smaller than maximum number of atoms")
        assert leftIdx<len(self.engine.pdb), LOGGER.error("angle atom index must be smaller than maximum number of atoms")
        assert rightIdx<len(self.engine.pdb), LOGGER.error("angle atom index must be smaller than maximum number of atoms")
        centralIdx = INT_TYPE(centralIdx)
        leftIdx    = INT_TYPE(leftIdx)
        rightIdx   = INT_TYPE(rightIdx)
        assert is_number(lower)
        lower = FLOAT_TYPE(lower)
        assert is_number(upper)
        upper = FLOAT_TYPE(upper)
        assert lower>=0, LOGGER.error("angle items lists fourth item must be positive")
        assert upper>lower, LOGGER.error("angle items lists fourth item must be smaller than the fifth item")
        assert upper<=180, LOGGER.error("angle items lists fifth item must be smaller or equal to 180")
        lower *= FLOAT_TYPE( PI/FLOAT_TYPE(180.) )
        upper *= FLOAT_TYPE( PI/FLOAT_TYPE(180.) )
        # append anglesMap definition where angles are in degrees
        self.__anglesMap.append( angle )
        # create atoms look up angles dictionary
        if not self.__atomsLUAD.has_key(centralIdx):
            self.__atomsLUAD[centralIdx] = []
        if not self.__atomsLUAD.has_key(leftIdx):
            self.__atomsLUAD[leftIdx] = []
        if not self.__atomsLUAD.has_key(rightIdx):
            self.__atomsLUAD[rightIdx] = []
        # create angles
        if not self.__angles.has_key(centralIdx):
            centralIdxToArray = False
            self.__angles[centralIdx] = {"leftIndexes":[],"rightIndexes":[],"lower":[],"upper":[]}
        else:
            centralIdxToArray = not isinstance(self.__angles[centralIdx]["leftIndexes"], list)
            self.__angles[centralIdx] = {"leftIndexes"  :list(self.__angles[centralIdx]["leftIndexes"]),
                                         "rightIndexes" :list(self.__angles[centralIdx]["rightIndexes"]),
                                         "lower"        :list(self.__angles[centralIdx]["lower"]),
                                         "upper"        :list(self.__angles[centralIdx]["upper"]) }
        # check for redundancy and append
        ignoreFlag=False
        if leftIdx in self.__angles[centralIdx]["leftIndexes"]:
            index = self.__angles[centralIdx]["leftIndexes"].index(leftIdx)
            if rightIdx == self.__angles[centralIdx]["rightIndexes"][index]:
                LOGGER.warn("Angle definition for central atom index '%i' and interchangeable left an right '%i' and '%i' is  already defined. New angle limits [%.3f,%.3f] are ignored and old angle limits [%.3f,%.3f] are kept."%(centralIdx, leftIdx, rightIdx, lower, upper, self.__angles[centralIdx]["lower"][index], self.__angles[centralIdx]["upper"][index]))
                ignoreFlag=True
        elif leftIdx in self.__angles[centralIdx]["rightIndexes"]:
            index = self.__angles[centralIdx]["rightIndexes"].index(leftIdx)
            if rightIdx == self.__angles[centralIdx]["leftIndexes"][index]:
                LOGGER.warn("Angle definition for central atom index '%i' and interchangeable left an right '%i' and '%i' is  already defined. New angle limits [%.3f,%.3f] are ignored and old angle limits [%.3f,%.3f] are kept."%(centralIdx, leftIdx, rightIdx, lower, upper, self.__angles[centralIdx]["lower"][index], self.__angles[centralIdx]["upper"][index]))
                ignoreFlag=True
        # add angle definition
        if not ignoreFlag:
            self.__angles[centralIdx]["leftIndexes"].append(leftIdx)
            self.__angles[centralIdx]["rightIndexes"].append(rightIdx)
            self.__angles[centralIdx]["lower"].append(lower)
            self.__angles[centralIdx]["upper"].append(upper)
            self.__atomsLUAD[centralIdx].append(centralIdx)
            self.__atomsLUAD[leftIdx].append(centralIdx)
            self.__atomsLUAD[rightIdx].append(centralIdx)
        if centralIdxToArray:
            angles = self.__angles.get(centralIdxToArray, {"leftIndexes":[],"rightIndexes":[],"lower":[],"upper":[]} )
            self.__angles[centralIdxToArray] =  {"leftIndexes"  : np.array(angles["leftIndexes"], dtype = INT_TYPE), 
                                                 "rightIndexes" : np.array(angles["rightIndexes"], dtype = INT_TYPE),
                                                 "lower"        : np.array(angles["lower"]  , dtype = FLOAT_TYPE),
                                                 "upper"        : np.array(angles["upper"]  , dtype = FLOAT_TYPE) }    
        # sort lookup tables
        lut = self.__atomsLUAD.get(centralIdx, [] )
        self.__atomsLUAD[centralIdx] = sorted(set(lut))
        lut = self.__atomsLUAD.get(leftIdx, [] )
        self.__atomsLUAD[leftIdx] = sorted(set(lut))
        lut = self.__atomsLUAD.get(rightIdx, [] )
        self.__atomsLUAD[rightIdx] = sorted(set(lut))
        # dump to repository
        if self.__dumpAngles:
            self._dump_to_repository({'_BondsAngleConstraint__anglesMap' :self.__anglesMap,
                                      '_BondsAngleConstraint__angles'    :self.__angles,
                                      '_BondsAngleConstraint__anglesLUAD':self.__atomsLUAD})

    def create_angles_by_definition(self, anglesDefinition):
        """ 
        Creates anglesMap using angles definition.
        Calls set_angles(anglesMap) and generates angles attribute.
        
        :Parameters:
            #. anglesDefinition (dict): The angles definition. 
               Every key must be a molecule name (residue name in pdb file). 
               Every key value must be a list of angles definitions. 
               Every angle definition is a list of five items where:
               
               #. First item: The name of the central atom forming the angle.
               #. Second item: The name of the left atom forming the angle (interchangeable with the right atom).
               #. Third item: The name of the right atom forming the angle (interchangeable with the left atom).
               #. Fourth item: The minimum lower limit or the minimum angle allowed 
                  in degrees which later will be converted to rad.
               #. Fifth item: The maximum upper limit or the maximum angle allowed 
                  in degrees which later will be converted to rad.
        
        ::
        
            e.g. (Carbon tetrachloride):  anglesDefinition={"CCL4": [('C','CL1','CL2' , 105, 115),
                                                                     ('C','CL2','CL3' , 105, 115),
                                                                     ('C','CL3','CL4' , 105, 115),                                      
                                                                     ('C','CL4','CL1' , 105, 115) ] }
                                                                 
        """
        if self.engine is None:
            raise Exception(LOGGER.error("Engine is not defined. Can't create angles by definition"))
        assert isinstance(anglesDefinition, dict), LOGGER.error("anglesDefinition must be a dictionary")
        # check map definition
        existingMoleculesNames = sorted(set(self.engine.moleculesNames))
        anglesDef = {}
        for mol, angles in anglesDefinition.items():
            if mol not in existingMoleculesNames:
                LOGGER.warn("Molecule name '%s' in anglesDefinition is not recognized, angles definition for this particular molecule is omitted"%str(mol))
                continue
            assert isinstance(angles, (list, set, tuple)), LOGGER.error("mapDefinition molecule angles must be a list")
            angles = list(angles)
            molAnglesMap = []
            for angle in angles:
                assert isinstance(angle, (list, set, tuple)), LOGGER.error("mapDefinition angles must be a list")
                angle = list(angle)
                assert len(angle)==5
                centralAt, leftAt, rightAt, lower, upper = angle
                # check for redundancy
                append = True
                for b in molAnglesMap:
                    if (b[0]==centralAt) and ( (b[1]==leftAt and b[2]==rightAt) or (b[1]==rightAt and b[2]==leftAt) ):
                        LOGGER.warn("Redundant definition for anglesDefinition found. The later '%s' is ignored"%str(b))
                        append = False
                        break
                if append:
                    molAnglesMap.append((centralAt, leftAt, rightAt, lower, upper))
            # create bondDef for molecule mol 
            anglesDef[mol] = molAnglesMap
        # create mols dictionary
        mols = {}
        for idx in self.engine.pdb.xindexes:
            molName = self.engine.moleculesNames[idx]
            if not molName in anglesDef.keys():    
                continue
            molIdx = self.engine.moleculesIndexes[idx]
            if not mols.has_key(molIdx):
                mols[molIdx] = {"name":molName, "indexes":[], "names":[]}
            mols[molIdx]["indexes"].append(idx)
            mols[molIdx]["names"].append(self.engine.allNames[idx])
        # get anglesMap
        anglesMap = []         
        for val in mols.values():
            indexes = val["indexes"]
            names   = val["names"]
            # get definition for this molecule
            thisDef = anglesDef[val["name"]]
            for angle in thisDef:
                centralIdx = indexes[ names.index(angle[0]) ]
                leftIdx    = indexes[ names.index(angle[1]) ]
                rightIdx   = indexes[ names.index(angle[2]) ]
                lower      = angle[3]
                upper      = angle[4]
                anglesMap.append((centralIdx, leftIdx, rightIdx, lower, upper))
        # create angles
        self.set_angles(anglesMap=anglesMap)
    
    def compute_standard_error(self, data):
        """ 
        Compute the standard error (StdErr) of data not satisfying constraint conditions. 
        
        .. math::
            StdErr = \\sum \\limits_{i}^{C} 
            ( \\theta_{i} - \\theta_{i}^{min} ) ^{2} 
            \\int_{0}^{\\theta_{i}^{min}} \\delta(\\theta-\\theta_{i}) d \\theta
            +
            ( \\theta_{i} - \\theta_{i}^{max} ) ^{2} 
            \\int_{\\theta_{i}^{max}}^{\\pi} \\delta(\\theta-\\theta_{i}) d \\theta
                               
        Where:\n
        :math:`C` is the total number of defined angles constraints. \n
        :math:`\\theta_{i}^{min}` is the angle constraint lower limit set for constraint i. \n
        :math:`\\theta_{i}^{max}` is the angle constraint upper limit set for constraint i. \n
        :math:`\\theta_{i}` is the angle computed for constraint i. \n
        :math:`\\delta` is the Dirac delta function. \n
        :math:`\\int_{0}^{\\theta_{i}^{min}} \\delta(\\theta-\\theta_{i}) d \\theta` 
        is equal to 1 if :math:`0 \\leqslant \\theta_{i} \\leqslant \\theta_{i}^{min}` and 0 elsewhere.\n
        :math:`\\int_{\\theta_{i}^{max}}^{\\pi} \\delta(\\theta-\\theta_{i}) d \\theta` 
        is equal to 1 if :math:`\\theta_{i}^{max} \\leqslant \\theta_{i} \\leqslant \\pi` and 0 elsewhere.\n

        :Parameters:
            #. data (numpy.array): The constraint value data to compute standardError.
            
        :Returns:
            #. standardError (number): The calculated standardError of the constraint.
        """
        standardError = 0
        for idx, angle in data.items():
            standardError +=  np.sum(angle["reducedAngles"]**2)
        return FLOAT_TYPE( standardError )

    def get_constraint_value(self):
        """
        Computes all partial Mean Pair Distances (MPD) below the defined minimum distance. 
        
        :Returns:
            #. MPD (dictionary): The MPD dictionary, where keys are the element wise intra and inter molecular MPDs and values are the computed MPDs.
        """
        return self.data
        
    def compute_data(self):
        """ Compute data and update engine constraintsData dictionary. """
        # get angles dictionary slice
        anglesIndexes = []
        for idx in self.engine.pdb.indexes:
            anglesIndexes.extend( self.__atomsLUAD[idx] )
        anglesDict = {}
        for idx in set(anglesIndexes):
            anglesDict[idx] = self.__angles[idx] 
        # compute data before move
        dataDict = full_angles_coords( anglesDict         = anglesDict ,
                                       boxCoords          = self.engine.boxCoordinates,
                                       basis              = self.engine.basisVectors ,
                                       isPBC              = self.engine.isPBC,
                                       reduceAngleToUpper = False,
                                       reduceAngleToLower = False,
                                       ncores             = INT_TYPE(1))
        self.set_data( dataDict )
        self.set_active_atoms_data_before_move(None)
        self.set_active_atoms_data_after_move(None)
        # set standardError
        #self.set_standard_error( self.compute_standard_error(data = dataDict) )
        
    def compute_before_move(self, indexes):
        """ 
        Compute constraint before move is executed.
        
        :Parameters:
            #. indexes (numpy.ndarray): Group atoms indexes the move will be applied to.
        """
        # get angles dictionary slice
        anglesIndexes = []
        for idx in indexes:
            anglesIndexes.extend( self.__atomsLUAD[idx] )
        anglesDict = {}
        for idx in set(anglesIndexes):
            anglesDict[idx] = self.angles[idx] 
        # compute data before move
        dataDict = full_angles_coords( anglesDict         = anglesDict ,
                                       boxCoords          = self.engine.boxCoordinates,
                                       basis              = self.engine.basisVectors ,
                                       isPBC              = self.engine.isPBC,
                                       reduceAngleToUpper = False,
                                       reduceAngleToLower = False,
                                       ncores             = INT_TYPE(1))
        # set data before move
        self.set_active_atoms_data_before_move( dataDict )
        self.set_active_atoms_data_after_move(None)
        
    def compute_after_move(self, indexes, movedBoxCoordinates):
        """ 
        Compute constraint after move is executed.
        
        :Parameters:
            #. indexes (numpy.ndarray): Group atoms indexes the move will be applied to.
            #. movedBoxCoordinates (numpy.ndarray): The moved atoms new coordinates.
        """
        # get angles dictionary slice
        anglesIndexes = []
        for idx in indexes:
            anglesIndexes.extend( self.__atomsLUAD[idx] )
        anglesDict = {}
        for idx in set(anglesIndexes):
            anglesDict[idx] = self.__angles[idx] 
        # change coordinates temporarily
        boxData = np.array(self.engine.boxCoordinates[indexes], dtype=FLOAT_TYPE)
        self.engine.boxCoordinates[indexes] = movedBoxCoordinates
        # compute data before move
        dataDict = full_angles_coords( anglesDict         = anglesDict ,
                                       boxCoords          = self.engine.boxCoordinates,
                                       basis              = self.engine.basisVectors ,
                                       isPBC              = self.engine.isPBC,
                                       reduceAngleToUpper = False,
                                       reduceAngleToLower = False,
                                       ncores             = INT_TYPE(1))
        # set data after move
        self.set_active_atoms_data_after_move( dataDict )
        # reset coordinates
        self.engine.boxCoordinates[indexes] = boxData
  
    def accept_move(self, indexes):
        """ 
        Accept move.
        
        :Parameters:
            #. indexes (numpy.ndarray): Group atoms indexes the move will be applied to.
        """
        # get indexes
        anglesIndexes = []
        for idx in indexes:
            anglesIndexes.extend( self.__atomsLUAD[idx] )
        for idx in set(anglesIndexes):
            self.data[idx]["angles"]        = self.activeAtomsDataAfterMove[idx]["angles"]
            self.data[idx]["reducedAngles"] = self.activeAtomsDataAfterMove[idx]["reducedAngles"]
        # reset activeAtoms data
        self.set_active_atoms_data_before_move(None)
        self.set_active_atoms_data_after_move(None)

    def reject_move(self, indexes):
        """ 
        Reject move.
        
        :Parameters:
            #. indexes (numpy.ndarray): Group atoms indexes the move will be applied to.
        """
        # reset activeAtoms data
        self.set_active_atoms_data_before_move(None)
        self.set_active_atoms_data_after_move(None)





        