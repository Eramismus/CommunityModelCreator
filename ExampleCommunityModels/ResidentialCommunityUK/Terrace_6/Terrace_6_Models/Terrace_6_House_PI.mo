 
within ResidentialCommunityUK.Terrace_6.Terrace_6_Models;
model Terrace_6_House_PI
  "This is the simulation model of House within building Terrace_6 with traceable ID None"
  
  parameter Real Ti=300;
  parameter Real Td=60;

  IBPSA.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
    calTSky=IBPSA.BoundaryConditions.Types.SkyTemperatureCalculation.HorizontalRadiation,
    computeWetBulbTemperature=false,
    filNam="C:/Users/cvrse/OneDrive - Loughborough University/SimDevEnv/Simulator_v7/Nottingham_TRY.mos")
    "Weather data reader"
    annotation (Placement(transformation(extent={{-98,52},{-78,72}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTil[2](
    each outSkyCon=true,
    each outGroCon=true,
    til={1.5707963267948966, 1.5707963267948966},
    each lat = 0.886452727088,
    azi = {1.5683195674375014, -1.573273086152292})
    "Calculates diffuse solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,20},{-48,40}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil[2](
    til={1.5707963267948966, 1.5707963267948966},
    each lat =  0.886452727088,
    azi={1.5683195674375014, -1.573273086152292})
    "Calculates direct solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,52},{-48,72}})));
  IBPSA.ThermalZones.ReducedOrder.SolarGain.CorrectionGDoublePane corGDoublePane(n=2,
  UWin=2.885646217986897)
    "Correction factor for solar transmission"
    annotation (Placement(transformation(extent={{6,54},{26,74}})));
  IBPSA.ThermalZones.ReducedOrder.RC.FourElements
  thermalZoneFourElements(
    redeclare package Medium = Modelica.Media.Air.DryAirNasa,
    VAir=187.36677387135808,
    alphaExt=3.000000000000001,
    alphaWin=3.0,
    gWin=0.84,
    ratioWinConRad=0.029999999999999995,
    nExt=1,
    RExt={0.0025550852647353507},
    CExt={6241720.023029091},
    alphaRad=5.970147188440039,
    AInt=170.64492735261973,
    alphaInt=3.0,
    nInt=1,
    RInt={0.0005180614494212665},
    CInt={11520818.203321688},
    RWin=0.020369863287610198,
    RExtRem=0.04849232263524709,
    AFloor=40.73190736333871,
    alphaFloor=3.0,
    nFloor=1,
    RFloor={0.002614426913889611},
    RFloorRem=0.003990901352416398,
    CFloor={15687085.39908305},
    ARoof=38.41516624254397,
    alphaRoof=4.3,
    nRoof=1,
    RRoof={0.009014824470772348},
    RRoofRem=0.1354939303209709,
    CRoof={996070.5266478816},
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    extWallRC(thermCapExt(each der_T(fixed=true))),
    intWallRC(thermCapInt(each der_T(fixed=true))),
    floorRC(thermCapExt(each der_T(fixed=true))),
    roofRC(thermCapExt(each der_T(fixed=true))),
    nOrientations=2,
    AWin={3.1692295099142362, 6.649196719860628},
    ATransparent={3.1692295099142362, 6.649196719860628},
    AExt={22.685385795895897, 19.365433900204735})
    "Thermal zone"
    annotation (Placement(transformation(extent={{44,-2},{92,34}})));
  IBPSA.ThermalZones.ReducedOrder.EquivalentAirTemperature.VDI6007WithWindow eqAirTemp(
    n=2,
    wfGro=0.0,
    wfWall={0.6366719736585754, 0.3633280263414245},
    wfWin={0.32278385922006425, 0.6772161407799357},
    withLongwave=true,
    aExt=0.9190798799329333,
    alphaWallOut=14.000000000000004,
    alphaRad=5.699999999999999,
    alphaWinOut=5.699999999999999,
    TGro=286.15) "Computes equivalent air temperature"
    annotation (Placement(transformation(extent={{-24,-14},{-4,6}})));
  Modelica.Blocks.Math.Add solRad[2]
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
  Modelica.Blocks.Sources.Constant const[2](each k=0)
    "Sets sunblind signal to zero (open)"
    annotation (Placement(transformation(extent={{-20,14},{-14,20}})));
  IBPSA.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(
    transformation(extent={{-100,-10},{-66,22}}),iconTransformation(
    extent={{-70,-12},{-50,8}})));
  Modelica.Blocks.Sources.Constant alphaWall(k=19.700000000000003*42.05081969610063)
    "Outdoor coefficient of heat transfer for walls"
    annotation (Placement(
    transformation(
    extent={{-4,-4},{4,4}},
    rotation=90,
    origin={30,-16})));
  Modelica.Blocks.Sources.Constant alphaWin(k=11.399999999999999*9.818426229774865)
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
  Modelica.Thermal.HeatTransfer.Sources.PrescribedHeatFlow machinesConv
    "Convective heat flow of machines"
    annotation (Placement(transformation(extent={{48,-84},{68,-64}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperatureFloor
    "Prescribed temperature for floor plate outdoor surface temperature"
    annotation (Placement(transformation(
    extent={{-6,-6},{6,6}},
    rotation=90,
    origin={67,-12})));
  Modelica.Blocks.Sources.Constant TSoil(k=286.15)
    "Outdoor surface temperature for floor plate"
    annotation (
    Placement(transformation(
    extent={{-4,-4},{4,4}},
    rotation=180,
    origin={84,-22})));

  IBPSA.ThermalZones.ReducedOrder.EquivalentAirTemperature.VDI6007 eqAirTempVDI(
    aExt=0.6,
    wfGro=0,
    alphaWallOut=18.1,
    alphaRad=5.699999999999999,
    n=4,
    wfWall={0.12581417111935222, 0.37418582888064783, 0.12581417111935222, 0.37418582888064783},
    wfWin={0, 0, 0, 0},
    TGro=285.15) "Computes equivalent air temperature for roof"
    annotation (Placement(transformation(extent={{30,34},{50,54}})));
  Modelica.Thermal.HeatTransfer.Sources.PrescribedTemperature prescribedTemperatureRoof
    "Prescribed temperature for roof outdoor surface temperature"
    annotation (Placement(transformation(extent={{-6,-6},{6,6}},rotation=-90,
    origin={67,44})));
  Modelica.Thermal.HeatTransfer.Components.Convection thermalConductorRoof
    "Outdoor convective heat transfer of roof"
    annotation (Placement(transformation(extent={{5,-5},{-5,5}},rotation=-90,
    origin={67,27})));
  Modelica.Blocks.Sources.Constant alphaRoof(k=914.2809565725463)
    "Outdoor coefficient of heat transfer for roof"
    annotation (Placement(transformation(extent={{4,-4},{-4,4}},rotation=0,
    origin={86,27})));
  Modelica.Blocks.Sources.Constant const1[4](each k=0)
    "Sets sunblind signal to zero (open)" annotation (Placement(transformation(
        extent={{3,-3},{-3,3}},
        rotation=90,
        origin={40,71})));
  Modelica.Blocks.Math.Add solRadRoof[4]
    "Sums up solar radiation of both directions"
    annotation (Placement(transformation(extent={{4,76},{14,86}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTilRoof[4](
    til={0.9599310885968813, 0.9599310885968813, 0.9599310885968813, 0.9599310885968813},
    each lat = 0.886452727088,
    azi={3.139115894232398, -1.573273086152292, -0.002476759357395301, 1.5683195674375014})
    "Calculates direct solar radiation on titled surface for both directions"
    annotation (Placement(transformation(extent={{-68,74},{-48,94}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTilRoof[4](
    til={0.9599310885968813, 0.9599310885968813, 0.9599310885968813, 0.9599310885968813},
    each lat = 0.886452727088,
    azi={3.139115894232398, -1.573273086152292, -0.002476759357395301, 1.5683195674375014})
    "Calculates diffuse solar radiation on titled surface for both directions"
    annotation (Placement(transformation(extent={{-68,48},{-48,68}})));
	
  Modelica.Blocks.Interfaces.RealInput RadGain
    annotation (Placement(transformation(extent={{-96,-68},{-72,-44}})));
  Modelica.Blocks.Interfaces.RealInput ConvGain1
    annotation (Placement(transformation(extent={{-78,-88},{-54,-64}})));
  Modelica.Blocks.Interfaces.RealInput SetPoint
    annotation (Placement(transformation(extent={{-70,-110},{-46,-86}})));
  Modelica.Blocks.Interfaces.RealOutput TAir
    annotation (Placement(transformation(extent={{112,36},{132,56}})));
  Modelica.Blocks.Interfaces.RealOutput HeatInput
    annotation (Placement(transformation(extent={{116,-76},{136,-56}})));	
  IBPSA.Controls.Continuous.PIDHysteresis conPID(Ti=Ti, Td=Td,
    initType=Modelica.Blocks.Types.InitPID.SteadyState,
    yMax=40000,
	k=1)
    annotation (Placement(transformation(extent={{-4,-96},{16,-76}})));	

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
  connect(personsRad.port, thermalZoneFourElements.intGainsRad)
    annotation (Line(
    points={{68,-32},{84,-32},{100,-32},{100,24},{92.2,24}},
    color={191,0,0}));
  connect(thermalConductorWin.solid, thermalZoneFourElements.window)
    annotation (
     Line(points={{38,21},{40,21},{40,20},{43.8,20}}, color={191,0,0}));
  connect(prescribedTemperature1.port, thermalConductorWin.fluid)
    annotation (Line(points={{20,20},{28,20},{28,21}}, color={191,0,0}));
  connect(thermalZoneFourElements.extWall, thermalConductorWall.solid)
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
  connect(machinesConv.port, thermalZoneFourElements.intGainsConv)
    annotation (
    Line(points={{68,-74},{82,-74},{96,-74},{96,20},{92,20}}, color={191,
    0,0}));
  connect(personsConv.port, thermalZoneFourElements.intGainsConv)
    annotation (
    Line(points={{68,-52},{96,-52},{96,20},{92,20}}, color={191,0,0}));
  connect(corGDoublePane.solarRadWinTrans, thermalZoneFourElements.solRad)
    annotation (Line(points={{27,64},{34,64},{40,64},{40,31},{43,31}}, color={0,
    0,127}));
  connect(prescribedTemperatureFloor.port, thermalZoneFourElements.floor)
    annotation (Line(points={{67,-6},{68,-6},{68,-2}}, color={191,0,0}));
  connect(prescribedTemperatureFloor.T, TSoil.y) annotation (Line(points={{67,-19.2},
          {72.5,-19.2},{72.5,-22},{79.6,-22}}, color={0,0,127}));
  connect(prescribedTemperatureRoof.port, thermalConductorRoof.fluid)
    annotation (Line(points={{67,38},{67,38},{67,32}}, color={191,0,0}));
  connect(thermalConductorRoof.solid, thermalZoneFourElements.roof)
    annotation (Line(points={{67,22},{66.8,22},{66.8,13}}, color={191,0,0}));
  connect(thermalConductorRoof.Gc, alphaRoof.y)
    annotation (Line(points={{72,27},{78,27},{81.6,27}},color={0,0,127}));
  connect(eqAirTempVDI.TDryBul, eqAirTemp.TDryBul)
    annotation (Line(points={{28,38},{-96,38},{-96,-36},{-38,-36},{-38,-44},{
          -26,-44}},
    color={0,0,127}));
  connect(eqAirTempVDI.TBlaSky, eqAirTemp.TBlaSky)
    annotation (Line(points={{28,44},{-34,44},{-98,44},{-98,-42},{-58,-42},{-58,
          -32},{-32,-32},{-32,-38},{-26,-38}},
    color={0,0,127}));
  connect(const1.y, eqAirTempVDI.sunblind)
    annotation (Line(points={{40,67.7},{40,56}}, color={0,0,127}));
  connect(eqAirTempVDI.TEqAir, prescribedTemperatureRoof.T) annotation (Line(
        points={{51,44},{56,44},{56,58},{67,58},{67,51.2}}, color={0,0,127}));
  connect(weaDat.weaBus, HDifTilRoof[1].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,58},{-68,58}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDirTilRoof[1].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,84},{-68,84}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDifTilRoof[2].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,58},{-68,58}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDirTilRoof[2].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,84},{-68,84}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDifTilRoof[3].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,58},{-68,58}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDirTilRoof[3].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,84},{-68,84}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDifTilRoof[4].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,58},{-68,58}},
      color={255,204,51},
      thickness=0.5));
  connect(weaDat.weaBus, HDirTilRoof[4].weaBus) annotation (Line(
      points={{-76,22},{-74,22},{-74,84},{-68,84}},
      color={255,204,51},
      thickness=0.5));
  connect(HDirTilRoof.H, solRadRoof.u1)
    annotation (Line(points={{-47,84},{-22,84},{3,84}}, color={0,0,127}));
  connect(HDifTilRoof.H, solRadRoof.u2) annotation (Line(points={{-47,58},{-22,
          58},{-22,78},{3,78}}, color={0,0,127}));
  connect(eqAirTempVDI.HSol, solRadRoof.y) annotation (Line(points={{28,50},
          {6,50},{6,46},{-83,46},{-83,6}}, color={0,0,127}), Text(
      string="%second",
      index=1,
      extent={{6,3},{6,3}}));
  connect(RadGain, personsRad.Q_flow) annotation (Line(points={{-84,-56},{8,-56},
          {8,-32},{48,-32}}, color={0,0,127}));
  connect(ConvGain1, personsConv.Q_flow) annotation (Line(points={{-66,-76},{-66,
          -64},{48,-64},{48,-52}}, color={0,0,127}));
  connect(thermalZoneFourElements.TAir, TAir) annotation (Line(points={{93,32},{
          102,32},{102,46},{122,46}}, color={0,0,127}));
  connect(SetPoint, conPID.u_s) annotation (Line(points={{-58,-98},{-32,-98},{-32,
          -86},{-6,-86}}, color={0,0,127}));
  connect(thermalZoneFourElements.TAir, conPID.u_m) annotation (Line(points={{93,
          32},{112,32},{112,-98},{6,-98}}, color={0,0,127}));
  connect(conPID.y, machinesConv.Q_flow) annotation (Line(points={{17,-86},{32,-86},
          {32,-74},{48,-74}}, color={0,0,127}));
  connect(conPID.y, HeatInput) annotation (Line(points={{17,-86},{60,-86},{60,-88},
          {104,-88},{104,-66},{126,-66}}, color={0,0,127}));
  annotation (experiment(
  StopTime=31536000,
  Interval=3600,
  __Dymola_Algorithm="Radau"),
  __Dymola_experimentSetupOutput(equidistant=true,
  events=false));
end Terrace_6_House_PI;
