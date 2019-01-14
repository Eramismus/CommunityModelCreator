 
within ResidentialCommunityUK_rad_2elements_example.SemiDetached_8.SemiDetached_8_Models;
model SemiDetached_8_House_PI
  "This is the simulation model of House within building SemiDetached_8 with traceable ID None"
  
  parameter Real Ti=1800;
  parameter Real Td=30;
  parameter Real kc=0.3;
  parameter Real COP_nominal = 2.5 "Nominal COP";
  parameter Modelica.SIunits.Power P_nominal=3000
    "Nominal compressor power (at y=1)";
  parameter Modelica.SIunits.TemperatureDifference dTEva_nominal=-10
    "Temperature difference evaporator outlet-inlet";
  parameter Modelica.SIunits.TemperatureDifference dTCon_nominal=10
    "Temperature difference condenser outlet-inlet";
  parameter Modelica.SIunits.MassFlowRate m2_flow_nominal=
     -P_nominal*(COP_nominal-1)/cp2_default/dTEva_nominal
    "Nominal mass flow rate at chilled water side";
  parameter Modelica.SIunits.MassFlowRate m1_flow_nominal=P_nominal*(COP_nominal-1)/cp1_default/dTCon_nominal;
  package Air = Modelica.Media.Air.DryAirNasa "air";
  package Water = Modelica.Media.Water.StandardWater "Water";
  
  IBPSA.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
    calTSky=IBPSA.BoundaryConditions.Types.SkyTemperatureCalculation.HorizontalRadiation,
    computeWetBulbTemperature=false,
    filNam="path_to_weather_folder/Nottingham_TRY.mos",
    totSkyCovSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    opaSkyCovSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    TDryBulSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    TDewPoiSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    TBlaSkySou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    relHumSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    winSpeSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    winDirSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    HInfHorSou=IBPSA.BoundaryConditions.Types.DataSource.Input,
    HSou=IBPSA.BoundaryConditions.Types.RadiationDataSource.Input_HGloHor_HDifHor,
    pAtmSou=IBPSA.BoundaryConditions.Types.DataSource.Parameter,
	ceiHeiSou=IBPSA.BoundaryConditions.Types.DataSource.Input)
    "Weather data reader"
    annotation (Placement(transformation(extent={{-98,58},{-78,76}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DiffusePerez
  HDifTil[7](
    each outSkyCon=true,
    each outGroCon=true,
    til={0.9599310885968813, 0.9599310885968813, 1.5707963267948966, 1.5707963267948966, 0.9599310885968813, 0.9599310885968813, 1.5707963267948966},
    each lat = 0.886452727088,
    azi = {-2.1123399040290436, -0.5415435772341476, -0.5415435772341476, 2.600049076355646, 2.600049076355646, 1.029252749560749, 1.029252749560749})
    "Calculates diffuse solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,20},{-48,40}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil[7](
    til={0.9599310885968813, 0.9599310885968813, 1.5707963267948966, 1.5707963267948966, 0.9599310885968813, 0.9599310885968813, 1.5707963267948966},
    each lat =  0.886452727088,
    azi={-2.1123399040290436, -0.5415435772341476, -0.5415435772341476, 2.600049076355646, 2.600049076355646, 1.029252749560749, 1.029252749560749})
    "Calculates direct solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,52},{-48,72}})));
  IBPSA.ThermalZones.ReducedOrder.SolarGain.CorrectionGDoublePane corGDoublePane(n=7,
  UWin=2.8856462179868974)
    "Correction factor for solar transmission"
    annotation (Placement(transformation(extent={{6,54},{26,74}})));
  IBPSA.ThermalZones.ReducedOrder.RC.TwoElements
  thermalZoneTwoElements(
    redeclare package Medium = Modelica.Media.Air.DryAirNasa,
    VAir=195.21585730651833,
    alphaExt=3.4989028382239926,
    alphaWin=3.000000000000001,
    gWin=0.84,
    ratioWinConRad=0.030000000000000002,
    nExt=1,
    RExt={0.001008322420263206},
    CExt={14867321.221708868},
    alphaRad=5.95895620070919,
    AInt=125.27090354631059,
    alphaInt=3.0,
    nInt=1,
    RInt={0.000781635887851082},
    CInt={7434798.830528043},
    RWin=0.019773885694664678,
    RExtRem=0.014136337141716734,
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    extWallRC(thermCapExt(each der_T(fixed=true))),
    intWallRC(thermCapInt(each der_T(fixed=true))),
    nOrientations=7,
    AWin={0.0, 0.0, 5.851096914586135, 3.5949412245488968, 0.0, 0.0, 0.6683118216298031},
    ATransparent={0.0, 0.0, 5.851096914586135, 3.5949412245488968, 0.0, 0.0, 0.6683118216298031},
    AExt={15.387583661713679, 12.8229863847614, 25.441445390086653, 27.852943062083934, 12.8229863847614, 15.387583661713679, 37.30203980934978})
    "Thermal zone"
    annotation (Placement(transformation(extent={{44,-2},{92,34}})));
  IBPSA.ThermalZones.ReducedOrder.EquivalentAirTemperature.VDI6007WithWindow eqAirTemp(
    n=7,
    wfGro=0.0,
    wfWall={0.04875476189506947, 0.040628968245891246, 0.2551330952218206, 0.2740156897954471, 0.040628968245891246, 0.04875476189506947, 0.29208375470081094},
    wfWin={0.0, 0.0, 0.578494607887157, 0.35542978426633876, 0.0, 0.0, 0.06607560784650426},
    withLongwave=true,
    aExt=0.7971085609063573,
    alphaWallOut=15.573462797475667,
    alphaRad=5.7,
    alphaWinOut=5.700000000000001,
    TGro=286.15) "Computes equivalent air temperature"
    annotation (Placement(transformation(extent={{-24,-14},{-4,6}})));
  Modelica.Blocks.Math.Add solRad[7]
    "Sums up solar radiation of both directions"
    annotation (Placement(transformation(extent={{-38,6},{-28,16}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature
    "Prescribed temperature for exterior walls outdoor surface temperature"
    annotation (Placement(transformation(extent={{8,-6},{20,6}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperature1
    "Prescribed temperature for windows outdoor surface temperature"
    annotation (Placement(transformation(extent={{8,14},{20,26}})));
  Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorWin
    "Outdoor convective heat transfer of windows"
    annotation (Placement(transformation(extent={{38,16},{28,26}})));
  Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorWall
    "Outdoor convective heat transfer of walls"
    annotation (Placement(transformation(extent={{36,6},{26,-4}})));
  Modelica.Blocks.Sources.Constant const[7](each k=0)
    "Sets sunblind signal to zero (open)"
    annotation (Placement(transformation(extent={{-20,14},{-14,20}})));
  IBPSA.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(
    transformation(extent={{-100,-10},{-66,22}}),iconTransformation(
    extent={{-70,-12},{-50,8}})));
  Modelica.Blocks.Sources.Constant alphaWall(k=21.27346279747567*147.01756835447054)
    "Outdoor coefficient of heat transfer for walls"
    annotation (Placement(
    transformation(
    extent={{-4,-4},{4,4}},
    rotation=90,
    origin={30,-16})));
  Modelica.Blocks.Sources.Constant alphaWin(k=11.400000000000002*10.114349960764834)
    "Outdoor coefficient of heat transfer for windows"
    annotation (Placement(
    transformation(
    extent={{4,-4},{-4,4}},
    rotation=90,
    origin={32,38})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow personsRad
    "Radiative heat flow of persons"
    annotation (Placement(transformation(extent={{48,-42},{68,-22}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow personsConv
    "Convective heat flow of persons"
    annotation (Placement(transformation(extent={{48,-62},{68,-42}})));
	
  Modelica.Blocks.Interfaces.RealInput RadGain
    annotation (Placement(transformation(extent={{-96,-68},{-72,-44}})));
  Modelica.Blocks.Interfaces.RealInput ConvGain1
    annotation (Placement(transformation(extent={{-78,-88},{-54,-64}})));
  Modelica.Blocks.Interfaces.RealOutput TAir
    annotation (Placement(transformation(extent={{112,36},{132,56}})));
  Modelica.Blocks.Interfaces.RealOutput PowerCompr
    annotation (Placement(transformation(extent={{108,-90},{128,-70}})));
 Modelica.Blocks.Interfaces.RealInput SetPoint
    annotation (Placement(transformation(extent={{-96,-68},{-72,-44}})));

  Modelica.Blocks.Interfaces.RealInput weaTDewPoi
    annotation (Placement(transformation(extent={{-144,122},{-120,146}})));
  Modelica.Blocks.Interfaces.RealInput weaTBlaSky
    annotation (Placement(transformation(extent={{-144,88},{-120,112}})));
  Modelica.Blocks.Interfaces.RealInput weaRelHum
    annotation (Placement(transformation(extent={{-144,72},{-120,96}})));
  Modelica.Blocks.Interfaces.RealInput weaOpaSkyCov
    annotation (Placement(transformation(extent={{-144,54},{-120,78}})));
  Modelica.Blocks.Interfaces.RealInput weaCeiHei
    annotation (Placement(transformation(extent={{-146,36},{-122,60}})));
  Modelica.Blocks.Interfaces.RealInput weaTotSkyCov
    annotation (Placement(transformation(extent={{-146,20},{-122,44}})));
  Modelica.Blocks.Interfaces.RealInput weaWinSpe
    annotation (Placement(transformation(extent={{-146,2},{-122,26}})));
  Modelica.Blocks.Interfaces.RealInput weaWinDir
    annotation (Placement(transformation(extent={{-146,-14},{-122,10}})));
  Modelica.Blocks.Interfaces.RealInput weaHInfHor
    annotation (Placement(transformation(extent={{-146,-30},{-122,-6}})));
  Modelica.Blocks.Interfaces.RealInput weaHDifHor
    annotation (Placement(transformation(extent={{-146,-46},{-122,-22}})));
  Modelica.Blocks.Interfaces.RealInput weaHGloHor
    annotation (Placement(transformation(extent={{-146,-62},{-122,-38}})));
  Modelica.Blocks.Interfaces.RealInput weaHDirNor
    annotation (Placement(transformation(extent={{-146,-78},{-122,-54}})));
  Modelica.Blocks.Interfaces.RealInput weaTDryBul
    annotation (Placement(transformation(extent={{-144,106},{-120,130}})));
	
  IBPSA.Controls.Continuous.PIDHysteresis conPID(Ti=Ti, Td=Td,
    initType=Modelica.Blocks.Types.InitPID.SteadyState,
 k=kc,
    controllerType=Modelica.Blocks.Types.SimpleController.PI,
    eOn=0.2)
    annotation (Placement(transformation(extent={{-4,-96},{16,-76}})));
	
IBPSA.Fluid.HeatPumps.Carnot_y heatpump(
    redeclare package Medium2 = Air,
    redeclare package Medium1 = Water,
    show_T=true,
    homotopyInitialization=true,
    from_dp1=false,
    tau1=60,
    P_nominal=P_nominal,
    dp1_nominal=100,
    dp2_nominal=100,
    etaCarnot_nominal=heatpump.COP_nominal/(heatpump.TUseAct_nominal/(heatpump.TCon_nominal
         + heatpump.TAppCon_nominal - (heatpump.TEva_nominal - heatpump.TAppEva_nominal))),
    COP_nominal=COP_nominal,
    a={0.8,0.2},
    m1_flow_nominal=m1_flow_nominal,
    m2_flow_nominal=m2_flow_nominal,
    dTEva_nominal=-10,
    dTCon_nominal=10)
    annotation (Placement(transformation(extent={{0,-92},{20,-72}})));

  Modelica.Fluid.Sources.Boundary_pT OutSideAir(
    redeclare package Medium = Air,
    nPorts=1,
    use_p_in=true,
    use_T_in=true)
    annotation (Placement(transformation(extent={{-26,-120},{-6,-100}})));
  Modelica.Blocks.Interfaces.RealOutput HeatInputAir
    annotation (Placement(transformation(extent={{126,-76},{146,-56}})));
  Modelica.Blocks.Interfaces.RealOutput HeatOutAir
    annotation (Placement(transformation(extent={{126,-114},{146,-94}})));
  Modelica.Fluid.Sources.MassFlowSource_T boundary(
    nPorts=1,
    redeclare package Medium = Air,
    use_m_flow_in=false,
    use_T_in=true,
    m_flow=m2_flow_nominal)          annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=180,
        origin={52,-110})));
	
  IBPSA.Fluid.HeatExchangers.Radiators.RadiatorEN442_2 rad(
    redeclare package Medium = Water,
    massDynamics=rad.energyDynamics,
    m_flow_nominal=m1_flow_nominal,
    Q_flow_nominal=P_nominal*COP_nominal,
    energyDynamics=Modelica.Fluid.Types.Dynamics.DynamicFreeInitial,
    dp_nominal(displayUnit="bar") = 20000,
    T_a_nominal(displayUnit="degC") = 328.15,
    T_b_nominal(displayUnit="degC") = 318.15,
	nEle=1)
    annotation (Placement(transformation(extent={{-10,-10},{10,10}},
        rotation=180,
        origin={-6,-44})));
		
  Modelica.Fluid.Machines.ControlledPump pump(
    m_flow_nominal=m1_flow_nominal,
    use_m_flow_set=false,
    redeclare package Medium = Water,
    m_flow_start=m1_flow_nominal,
    use_T_start=true,
    p_a_start=100000,
    p_b_start=120000,
    T_start=Water.T_default,
    p_a_nominal=100000,
    p_b_nominal=130000)
    annotation (Placement(transformation(extent={{-78,-136},{-58,-116}})));

  final parameter Modelica.SIunits.SpecificHeatCapacity cp1_default=
    Water.specificHeatCapacityCp(Water.setState_pTX(
      Water.p_default,
      Water.T_default,
      Water.X_default));

  final parameter Modelica.SIunits.SpecificHeatCapacity cp2_default=
    Air.specificHeatCapacityCp(Air.setState_pTX(
      Air.p_default,
      Air.T_default,
      Air.X_default));
  

	
equation
  connect(eqAirTemp.TEqAirWin, prescribedTemperature1.T)
    annotation (Line(
    points={{-3,-0.2},{0,-0.2},{0,20},{6.8,20}},   color={0,0,127}));
  connect(eqAirTemp.TEqAir, prescribedTemperature.T)
    annotation (Line(points={{-3,-4},{4,-4},{4,0},{6.8,0}},
    color={0,0,127}));
  connect(weaDat.weaBus, weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,18},{-84,18},{-84,12},{-83,12},{-83,6}},
    color={255,204,51},
    thickness=0.5), Text(
    string="%second",
    index=1,
    extent={{6,3},{6,3}}));
  connect(weaBus.TDryBul, eqAirTemp.TDryBul)
    annotation (Line(
    points={{-83,6},{-83,-2},{-38,-2},{-38,-10},{-26,-10}},
    color={255,204,51},
    thickness=0.5), Text(
    string="%first",
    index=-1,
    extent={{-6,3},{-6,3}}));
  connect(const.y, eqAirTemp.sunblind)
    annotation (Line(points={{-13.7,17},{-12,17},{-12,8},{-14,8},{-14,8}},
    color={0,0,127}));
  connect(HDifTil.HSkyDifTil, corGDoublePane.HSkyDifTil)
    annotation (Line(
    points={{-47,36},{-28,36},{-6,36},{-6,66},{4,66}}, color={0,0,127}));
  connect(HDirTil.H, corGDoublePane.HDirTil)
    annotation (Line(points={{-47,62},{-10,62},{-10,70},{4,70}},
    color={0,0,127}));
  connect(HDirTil.H,solRad. u1)
    annotation (Line(points={{-47,62},{-42,62},{-42,
    14},{-39,14}}, color={0,0,127}));
  connect(HDirTil.inc, corGDoublePane.inc)
    annotation (Line(points={{-47,58},{4,58},{4,58}}, color={0,0,127}));
  connect(HDifTil.H,solRad. u2)
    annotation (Line(points={{-47,30},{-44,30},{-44,
    8},{-39,8}}, color={0,0,127}));
  connect(HDifTil.HGroDifTil, corGDoublePane.HGroDifTil)
    annotation (Line(
    points={{-47,24},{-4,24},{-4,62},{4,62}}, color={0,0,127}));
  connect(solRad.y, eqAirTemp.HSol)
    annotation (Line(points={{-27.5,11},{-26,11},{-26,2},{-26,2}},
    color={0,0,127}));
    connect(weaDat.weaBus, HDifTil[1].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[1].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[2].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[2].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[3].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[3].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[4].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[4].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[5].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[5].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[6].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[6].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDifTil[7].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[7].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
  connect(personsRad.port, thermalZoneTwoElements.intGainsRad)
    annotation (Line(
    points={{68,-32},{84,-32},{100,-32},{100,24},{92.2,24}},
    color={191,0,0}));
  connect(thermalConductorWin.solid, thermalZoneTwoElements.window)
    annotation (
     Line(points={{38,21},{40,21},{40,20},{43.8,20}}, color={191,0,0}));
  connect(prescribedTemperature1.port, thermalConductorWin.fluid)
    annotation (Line(points={{20,20},{28,20},{28,21}}, color={191,0,0}));
  connect(thermalZoneTwoElements.extWall, thermalConductorWall.solid)
    annotation (Line(points={{43.8,12},{40,12},{40,1},{36,1}},
    color={191,0,0}));
  connect(thermalConductorWall.fluid, prescribedTemperature.port)
    annotation (Line(points={{26,1},{24,1},{24,0},{20,0}}, color={191,0,0}));
  connect(alphaWall.y, thermalConductorWall.Gc)
    annotation (Line(points={{30,-11.6},{30,-4},{31,-4}}, color={0,0,127}));
  connect(alphaWin.y, thermalConductorWin.Gc)
    annotation (Line(points={{32,33.6},{32,26},{33,26}}, color={0,0,127}));
  connect(weaBus.TBlaSky, eqAirTemp.TBlaSky)
    annotation (Line(
    points={{-83,6},{-58,6},{-58,2},{-32,2},{-32,-4},{-26,-4}},
    color={255,204,51},
    thickness=0.5), Text(
    string="%first",
    index=-1,
    extent={{-6,3},{-6,3}}));
  connect(personsConv.port, thermalZoneTwoElements.intGainsConv)
    annotation (
    Line(points={{68,-52},{96,-52},{96,20},{92,20}}, color={191,0,0}));
  connect(corGDoublePane.solarRadWinTrans, thermalZoneTwoElements.solRad)
    annotation (Line(points={{27,64},{34,64},{40,64},{40,31},{43,31}}, color={0,
    0,127}));
  connect(RadGain, personsRad.Q_flow) annotation (Line(points={{-84,-56},{8,-56},
          {8,-32},{48,-32}}, color={0,0,127}));
  connect(ConvGain1, personsConv.Q_flow) annotation (Line(points={{-66,-76},{-66,
          -64},{48,-64},{48,-52}}, color={0,0,127}));
  connect(thermalZoneTwoElements.TAir, TAir) annotation (Line(points={{93,32},{
          102,32},{102,46},{122,46}}, color={0,0,127}));
  connect(thermalZoneTwoElements.TAir, conPID.u_m) annotation (Line(points={{93,32},
          {112,32},{112,-94},{-70,-94}},   color={0,0,127}));
  connect(heatpump.P, PowerCompr) annotation (Line(points={{21,-82},{64,-82},{
          64,-86},{96,-86},{96,-82},{136,-82}},color={0,0,127}));
  connect(conPID.y, heatpump.y) annotation (Line(points={{-59,-82},{-30,-82},{-30,
          -73},{-2,-73}},color={0,0,127}));
  connect(OutSideAir.ports[1], heatpump.port_b2) annotation (Line(points={{-6,-110},
          {-2,-110},{-2,-88},{0,-88}}, color={0,127,255}));
  connect(heatpump.QCon_flow, HeatInputAir) annotation (Line(points={{21,-73},{70,
          -73},{70,-74},{118,-74},{118,-66},{136,-66}},
                                      color={0,0,127}));
  connect(heatpump.QEva_flow, HeatOutAir) annotation (Line(points={{21,-91},{
          74.5,-91},{74.5,-104},{136,-104}},
                                        color={0,0,127}));
  connect(boundary.ports[1], heatpump.port_a2) annotation (Line(points={{42,-110},
          {36,-110},{36,-88},{20,-88}}, color={0,127,255}));
  connect(weaBus.TDryBul, boundary.T_in) annotation (Line(
      points={{-83,6},{-58,6},{-58,-2},{-48,-2},{-48,-134},{82,-134},{82,-114},{
          64,-114}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.pAtm, OutSideAir.p_in) annotation (Line(
      points={{-83,6},{-83,-48},{-28,-48},{-28,-102}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
  connect(weaBus.TDryBul, OutSideAir.T_in) annotation (Line(
      points={{-83,6},{-56,6},{-56,-106},{-28,-106}},
      color={255,204,51},
      thickness=0.5), Text(
      string="%first",
      index=-1,
      extent={{-6,3},{-6,3}}));
connect(heatpump.port_b1, rad.port_a) annotation (Line(points={{20,-76},{30,-76},
          {30,-44},{4,-44}}, color={0,127,255}));
  connect(rad.port_b, pump.port_a) annotation (Line(points={{-16,-44},{-96,-44},
          {-96,-124},{-88,-124},{-88,-126},{-78,-126}}, color={0,127,255}));
  connect(pump.port_b, heatpump.port_a1) annotation (Line(points={{-58,-126},{-30,
          -126},{-30,-76},{0,-76}}, color={0,127,255}));
  connect(rad.heatPortCon, thermalZoneTwoElements.intGainsConv) annotation (
      Line(points={{-4,-51.2},{44,-51.2},{44,20},{92,20}}, color={191,0,0}));
  connect(rad.heatPortRad, thermalZoneTwoElements.intGainsRad) annotation (
      Line(points={{-8,-51.2},{42,-51.2},{42,24},{92,24}}, color={191,0,0}));
  
  connect(weaTDewPoi, weaDat.TDewPoi_in) annotation (Line(points={{-132,134},{-116,
          134},{-116,77.08},{-99,77.08}},      color={0,0,127}));
  connect(weaTDryBul, weaDat.TDryBul_in) annotation (Line(points={{-132,118},{-114,
          118},{-114,138},{-108,138},{-108,75.1},{-99,75.1}},      color={0,0,127}));
  connect(weaTBlaSky, weaDat.TBlaSky_in) annotation (Line(points={{-132,100},{-114,
          100},{-114,128},{-108,128},{-108,73.3},{-99,73.3}},      color={0,0,127}));
  connect(weaRelHum, weaDat.relHum_in) annotation (Line(points={{-132,84},{-118,
          84},{-118,71.5},{-99,71.5}},  color={0,0,127}));
  connect(weaOpaSkyCov, weaDat.opaSkyCov_in) annotation (Line(points={{-132,66},
          {-118,66},{-118,69.34},{-99,69.34}},      color={0,0,127}));
  connect(weaCeiHei, weaDat.ceiHei_in) annotation (Line(points={{-134,48},{-120,
          48},{-120,67.27},{-99.1,67.27}},     color={0,0,127}));
  connect(weaTotSkyCov, weaDat.totSkyCov_in) annotation (Line(points={{-134,32},
          {-120,32},{-120,65.29},{-99,65.29}},    color={0,0,127}));
  connect(weaWinSpe, weaDat.winSpe_in) annotation (Line(points={{-134,14},{-120,
          14},{-120,63.49},{-99,63.49}},    color={0,0,127}));
  connect(weaWinDir, weaDat.winDir_in) annotation (Line(points={{-134,-2},{-120,
          -2},{-120,61.6},{-99,61.6}},    color={0,0,127}));
  connect(weaHDifHor, weaDat.HDifHor_in) annotation (Line(points={{-134,-34},{-124,
          -34},{-124,-32},{-114,-32},{-114,60.16},{-99,60.16}},    color={0,0,127}));
  connect(weaHInfHor, weaDat.HInfHor_in) annotation (Line(points={{-134,-18},{-116,
          -18},{-116,58.45},{-99,58.45}},  color={0,0,127}));
  connect(weaHGloHor, weaDat.HGloHor_in) annotation (Line(points={{-134,-50},{-112,
          -50},{-112,55.3},{-99,55.3}},    color={0,0,127}));
  connect(weaHDirNor, weaDat.HDirNor_in);
  
   connect(SetPoint, conPID.u_s);
  
  annotation (experiment(
  StopTime=31536000,
  Interval=3600,
  __Dymola_Algorithm="Radau"),
  __Dymola_experimentSetupOutput(equidistant=true,
  events=false));
end SemiDetached_8_House_PI;
