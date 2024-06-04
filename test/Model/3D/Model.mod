'# MWS Version: Version 2024.4 - Apr 30 2024 - ACIS 33.0.1 -

'# length = um
'# frequency = THz
'# time = ns
'# frequency range: fmin = 0.100000 fmax = 2.000000
'# created = '[VERSION]2024.4|33.0.1|20240430[/VERSION]


'@ Units

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Units
.Geometry "um"
.Frequency "THz"
.Voltage "V"
.Resistance "Ohm"
.Inductance "H"
.TemperatureUnit  "Kelvin"
.Time "ns"
.Current "A"
.Conductance "Siemens"
.Capacitance "F"
End With
ThermalSolver.AmbientTemperature "0"

'@ Ambient Temperature

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
ThermalSolver.AmbientTemperature "0"

'@ Frequency Range

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
Solver.FrequencyRange "0.100000","2.000000"

'@ Draw Box

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
Plot.DrawBox True

'@ Background

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Background
.Type "Normal"
.Epsilon "1.0"
.Mu "1.0"
.Rho "1.204"
.ThermalType "Normal"
.ThermalConductivity "0.026"
.SpecificHeat "1005", "J/K/kg"
.XminSpace "0.0"
.XmaxSpace "0.0"
.YminSpace "0.0"
.YmaxSpace "0.0"
.ZminSpace "0.0"
.ZmaxSpace "0.0"
End With

'@ Floquet Port

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With FloquetPort
.Reset
.SetDialogTheta "0"
.SetDialogPhi "0"
.SetSortCode "+beta/pw"
.SetCustomizedListFlag "False"
.Port "Zmin"
.SetNumberOfModesConsidered "2"
.Port "Zmax"
.SetNumberOfModesConsidered "2"
End With

'@ Parameter

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
MakeSureParameterExists "theta", "0"
SetParameterDescription "theta", "spherical angle of incident plane wave"
MakeSureParameterExists "phi", "0"
SetParameterDescription "phi", "spherical angle of incident plane wave"

'@ Boundary

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Boundary
.Xmin "unit cell"
.Xmax "unit cell"
.Ymin "unit cell"
.Ymax "unit cell"
.Zmin "expanded open"
.Zmax "expanded open"
.Xsymmetry "none"
.Ysymmetry "none"
.Zsymmetry "none"
.XPeriodicShift "0.0"
.YPeriodicShift "0.0"
.ZPeriodicShift "0.0"
.PeriodicUseConstantAngles "False"
.SetPeriodicBoundaryAngles "theta", "phi"
.SetPeriodicBoundaryAnglesDirection "inward"
.UnitCellFitToBoundingBox "True"
.UnitCellDs1 "0.0"
.UnitCellDs2 "0.0"
.UnitCellAngle "90.0"
End With

'@ Mesh

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Mesh
.MeshType "Tetrahedral"
End With

'@ FDSolver

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With FDSolver
.Reset
.SetMethod "Tetrahedral", "General purpose"
.OrderTet "Second"
.OrderSrf "First"
.Stimulation "Zmax", "TM(0,0)"
.ResetExcitationList
.AddToExcitationList "Zmax", "TE(0,0);TM(0,0)"
.AutoNormImpedance "False"
.NormingImpedance "50"
.ModesOnly "False"
.ConsiderPortLossesTet "True"
.SetShieldAllPorts "False"
.AccuracyHex "1e-6"
.AccuracyTet "1e-4"
.AccuracySrf "1e-3"
.LimitIterations "False"
.MaxIterations "0"
.SetCalcBlockExcitationsInParallel "True", "True", ""
.StoreAllResults "False"
.StoreResultsInCache "False"
.UseHelmholtzEquation "True"
.LowFrequencyStabilization "False"
.Type "Direct"
.MeshAdaptionHex "False"
.MeshAdaptionTet "True"
.AcceleratedRestart "True"
.FreqDistAdaptMode "Distributed"
.NewIterativeSolver "True"
.TDCompatibleMaterials "False"
.ExtrudeOpenBC "False"
.SetOpenBCTypeHex "Default"
.SetOpenBCTypeTet "Default"
.AddMonitorSamples "True"
.CalcPowerLoss "True"
.CalcPowerLossPerComponent "False"
.SetKeepSolutionCoefficients "MonitorsAndMeshAdaptation"
.UseDoublePrecision "False"
.UseDoublePrecision_ML "True"
.MixedOrderSrf "False"
.MixedOrderTet "False"
.PreconditionerAccuracyIntEq "0.15"
.MLFMMAccuracy "Default"
.MinMLFMMBoxSize "0.3"
.UseCFIEForCPECIntEq "True"
.UseEnhancedCFIE2 "True"
.UseFastRCSSweepIntEq "false"
.UseSensitivityAnalysis "False"
.UseEnhancedNFSImprint "True"
.UseFastDirectFFCalc "False"
.RemoveAllStopCriteria "Hex"
.AddStopCriterion "All S-Parameters", "0.01", "2", "Hex", "True"
.AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Hex", "False"
.AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Hex", "False"
.RemoveAllStopCriteria "Tet"
.AddStopCriterion "All S-Parameters", "0.01", "2", "Tet", "True"
.AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Tet", "False"
.AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Tet", "False"
.AddStopCriterion "All Probes", "0.05", "2", "Tet", "True"
.RemoveAllStopCriteria "Srf"
.AddStopCriterion "All S-Parameters", "0.01", "2", "Srf", "True"
.AddStopCriterion "Reflection S-Parameters", "0.01", "2", "Srf", "False"
.AddStopCriterion "Transmission S-Parameters", "0.01", "2", "Srf", "False"
.SweepMinimumSamples "3"
.SetNumberOfResultDataSamples "1000"
.SetResultDataSamplingMode "Automatic"
.SweepWeightEvanescent "1.0"
.AccuracyROM "1e-4"
.AddSampleInterval "", "", "1", "Automatic", "True"
.AddSampleInterval "", "", "", "Automatic", "False"
.MPIParallelization "False"
.UseDistributedComputing "False"
.NetworkComputingStrategy "RunRemote"
.NetworkComputingJobCount "3"
.UseParallelization "True"
.MaxCPUs "1024"
.MaximumNumberOfCPUDevices "1"
End With

'@ IESolver

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With IESolver
.Reset
.UseFastFrequencySweep "True"
.UseIEGroundPlane "False"
.SetRealGroundMaterialName ""
.CalcFarFieldInRealGround "False"
.RealGroundModelType "Auto"
.PreconditionerType "Auto"
.ExtendThinWireModelByWireNubs "False"
.ExtraPreconditioning "False"
End With

'@ IESolver Additional

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With IESolver
.SetFMMFFCalcStopLevel "0"
.SetFMMFFCalcNumInterpPoints "6"
.UseFMMFarfieldCalc "True"
.SetCFIEAlpha "0.500000"
.LowFrequencyStabilization "False"
.LowFrequencyStabilizationML "True"
.Multilayer "False"
.SetiMoMACC_I "0.0001"
.SetiMoMACC_M "0.0001"
.DeembedExternalPorts "True"
.SetOpenBC_XY "True"
.OldRCSSweepDefintion "False"
.SetRCSOptimizationProperties "True", "100", "0.00001"
.SetAccuracySetting "Custom"
.CalculateSParaforFieldsources "True"
.ModeTrackingCMA "True"
.NumberOfModesCMA "3"
.StartFrequencyCMA "-1.0"
.SetAccuracySettingCMA "Default"
.FrequencySamplesCMA "0"
.SetMemSettingCMA "Auto"
.CalculateModalWeightingCoefficientsCMA "True"
.DetectThinDielectrics "True"
End With

'@ MeshSettings

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With MeshSettings
.SetMeshType "Tet"
.Set "Version", 1
End With

'@ Change Solver Type

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
ChangeSolverType("HF Frequency Domain")

'@ define PI

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Material
.Reset
.Name "Polyimide (lossy)"
.Folder ""
.FrqType "all"
.Type "Normal"
.SetMaterialUnit "MHz", "mm"
.Epsilon "3.5"
.Mu "1.0"
.Kappa "0.0"
.TanD "0.0027"
.TanDFreq "1.0"
.TanDGiven "True"
.TanDModel "ConstTanD"
.KappaM "0.0"
.TanDM "0.0"
.TanDMFreq "0.0"
.TanDMGiven "False"
.TanDMModel "ConstKappa"
.DispModelEps "None"
.DispModelMu "None"
.DispersiveFittingSchemeEps "General 1st"
.DispersiveFittingSchemeMu "General 1st"
.UseGeneralDispersionEps "False"
.UseGeneralDispersionMu "False"
.Rho "1400.0"
.ThermalType "Normal"
.ThermalConductivity "0.20"
.SpecificHeat "1000", "J/K/kg"
.SetActiveMaterial "all"
.MechanicsType "Isotropic"
.YoungsModulus "2.5"
.PoissonsRatio "0.4"
.ThermalExpansionRate "25"
.Colour "0.94", "0.82", "0.76"
.Wireframe "False"
.Transparency "0"
.Create
End With

'@ define AL

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Material
.Reset
.Name "Aluminum"
.Folder ""
.FrqType "static"
.Type "Normal"
.SetMaterialUnit "Hz", "mm"
.Epsilon "1"
.Mu "1.0"
.Kappa "3.56e+007"
.TanD "0.0"
.TanDFreq "0.0"
.TanDGiven "False"
.TanDModel "ConstTanD"
.KappaM "0"
.TanDM "0.0"
.TanDMFreq "0.0"
.TanDMGiven "False"
.TanDMModel "ConstTanD"
.DispModelEps "None"
.DispModelMu "None"
.DispersiveFittingSchemeEps "General 1st"
.DispersiveFittingSchemeMu "General 1st"
.UseGeneralDispersionEps "False"
.UseGeneralDispersionMu "False"
.FrqType "all"
.Type "Lossy metal"
.MaterialUnit "Frequency", "GHz"
.MaterialUnit "Geometry", "mm"
.MaterialUnit "Time", "s"
.MaterialUnit "Temperature", "Kelvin"
.Mu "1.0"
.Sigma "3.56e+007"
.Rho "2700.0"
.ThermalType "Normal"
.ThermalConductivity "237.0"
.SpecificHeat "900", "J/K/kg"
.MetabolicRate "0"
.BloodFlow "0"
.VoxelConvection "0"
.MechanicsType "Isotropic"
.YoungsModulus "69"
.PoissonsRatio "0.33"
.ThermalExpansionRate "23"
.ReferenceCoordSystem "Global"
.CoordSystemType "Cartesian"
.NLAnisotropy "False"
.NLAStackingFactor "1"
.NLADirectionX "1"
.NLADirectionY "0"
.NLADirectionZ "0"
.Colour "1", "1", "0"
.Wireframe "False"
.Reflection "False"
.Allowoutline "True"
.Transparentoutline "False"
.Transparency "0"
.Create
End With

'@ StoreParameter

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
StoreParameter("P","220.000000")

'@ global_WCS

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
WCS.ActivateWCS "global"

'@ Brick

'[VERSION]2024.4|33.0.1|20240430[/VERSION]
With Brick
.Reset
.Name "sub" 
.Component "PI" 
.Material "Polyimide (lossy)"
.Xrange "-P/2", "P/2"
.Yrange "-P/2", "P/2"
.Zrange "0", "30"
.Create
End With

