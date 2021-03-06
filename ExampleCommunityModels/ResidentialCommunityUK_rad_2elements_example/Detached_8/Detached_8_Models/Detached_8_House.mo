 
within ResidentialCommunityUK_rad_2elements_example.Detached_8.Detached_8_Models;
model Detached_8_House
  "This is the simulation model of House within building Detached_8 with traceable ID None"

  IBPSA.BoundaryConditions.WeatherData.ReaderTMY3 weaDat(
    calTSky=IBPSA.BoundaryConditions.Types.SkyTemperatureCalculation.HorizontalRadiation,
    computeWetBulbTemperature=false,
    filNam="path_to_weather_folder/Nottingham_TRY.mos")
    "Weather data reader"
    annotation (Placement(transformation(extent={{-98,52},{-78,72}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTil[8](
    each outSkyCon=true,
    each outGroCon=true,
    til={1.5707963267948966, 0.9599310885968813, 0.9599310885968813, 0.9599310885968813, 1.5707963267948966, 0.9599310885968813, 1.5707963267948966, 1.5707963267948966},
    each lat = 0.886452727088,
    azi = {2.8549276819542273, 2.8549276819542273, 1.284131355159331, -0.2866649716355655, 1.284131355159331, -1.8574612984304621, -1.8574612984304621, -0.2866649716355655})
    "Calculates diffuse solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,20},{-48,40}})));
  IBPSA.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil[8](
    til={1.5707963267948966, 0.9599310885968813, 0.9599310885968813, 0.9599310885968813, 1.5707963267948966, 0.9599310885968813, 1.5707963267948966, 1.5707963267948966},
    each lat =  0.886452727088,
    azi={2.8549276819542273, 2.8549276819542273, 1.284131355159331, -0.2866649716355655, 1.284131355159331, -1.8574612984304621, -1.8574612984304621, -0.2866649716355655})
    "Calculates direct solar radiation on titled surface for all directions"
    annotation (Placement(transformation(extent={{-68,52},{-48,72}})));
  IBPSA.ThermalZones.ReducedOrder.SolarGain.CorrectionGDoublePane corGDoublePane(n=8,
  UWin=2.8856462179868965)
    "Correction factor for solar transmission"
    annotation (Placement(transformation(extent={{6,54},{26,74}})));
  IBPSA.ThermalZones.ReducedOrder.RC.ThreeElements
  thermalZoneThreeElements(
    redeclare package Medium = Modelica.Media.Air.DryAirNasa,
    VAir=240.16716679998865,
    alphaExt=3.5215636758573226,
    alphaWin=2.999999999999999,
    gWin=0.84,
    ratioWinConRad=0.03,
    nExt=1,
    RExt={0.0007675751939837331},
    CExt={19527728.86519492},
    alphaRad=5.986031067290888,
    AInt=131.95385310772969,
    alphaInt=3.000000000000001,
    nInt=1,
    RInt={0.0007784335179540225},
    CInt={7357991.646143382},
    RWin=0.014713254429989636,
    RExtRem=0.010912896311157473,
    AFloor=50.94254058676101,
    alphaFloor=3.0,
    nFloor=1,
    RFloor={0.002090406046463376},
    RFloorRem=0.0031909877738821165,
    CFloor={19619508.055496864},
    energyDynamics=Modelica.Fluid.Types.Dynamics.FixedInitial,
    extWallRC(thermCapExt(each der_T(fixed=true))),
    intWallRC(thermCapInt(each der_T(fixed=true))),
    floorRC(thermCapExt(each der_T(fixed=true))),
    nOrientations=8,
    AWin={0.7077116264026388, 0.0, 0.0, 0.0, 5.271194370111608, 0.0, 7.614279722638773, 0.0},
    ATransparent={0.7077116264026388, 0.0, 0.0, 0.0, 5.271194370111608, 0.0, 7.614279722638773, 0.0},
    AExt={34.78730172055103, 24.346060412406274, 15.36401870685833, 24.346060412406274, 25.662628802903072, 15.36401870685833, 23.297740384999006, 34.78730172055103})
    "Thermal zone"
    annotation (Placement(transformation(extent={{44,-2},{92,34}})));
  IBPSA.ThermalZones.ReducedOrder.EquivalentAirTemperature.VDI6007WithWindow eqAirTemp(
    n=8,
    wfGro=0.0,
    wfWall={0.2419652264495486, 0.05931514395538263, 0.03743188696213467, 0.05931514395538263, 0.1900680456028298, 0.03743188696213467, 0.1325074396630384, 0.2419652264495486},
    wfWin={0.052063706111618986, 0.0, 0.0, 0.0, 0.3877821195869052, 0.0, 0.560154174301476, 0.0},
    withLongwave=true,
    aExt=0.7906439141141806,
    alphaWallOut=15.644931593088478,
    alphaRad=5.7,
    alphaWinOut=5.7,
    TGro=286.15) "Computes equivalent air temperature"
    annotation (Placement(transformation(extent={{-24,-14},{-4,6}})));
  Modelica.Blocks.Math.Add solRad[8]
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
  Modelica.Blocks.Sources.Constant const[8](each k=0)
    "Sets sunblind signal to zero (open)"
    annotation (Placement(transformation(extent={{-20,14},{-14,20}})));
  IBPSA.BoundaryConditions.WeatherData.Bus weaBus "Weather data bus"
    annotation (Placement(
    transformation(extent={{-100,-10},{-66,22}}),iconTransformation(
    extent={{-70,-12},{-50,8}})));
  Modelica.Blocks.Sources.Constant alphaWall(k=21.344931593088475*197.95513086753334)
    "Outdoor coefficient of heat transfer for walls"
    annotation (Placement(
    transformation(
    extent={{-4,-4},{4,4}},
    rotation=90,
    origin={30,-16})));
  Modelica.Blocks.Sources.Constant alphaWin(k=11.4*13.59318571915302)
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
  Modelica.Blocks.Sources.CombiTimeTable internalGains(
    tableOnFile=true,
    extrapolation=Modelica.Blocks.Types.Extrapolation.Periodic,
    tableName="Internals",
    fileName=Modelica.Utilities.Files.loadResource(
      "modelica://ResidentialCommunityUK_rad_2elements_example/Detached_8/Detached_8_Models/InternalGains_Detached_8House.mat"),
    columns={2,3,4})
    "Table with profiles for persons (radiative and convective) and machines (convective)"
    annotation (Placement(transformation(extent={{6,-60},{22,-44}})));
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
  connect(internalGains.y[1], personsRad.Q_flow)
    annotation (Line(points={{22.8,
    -52},{28,-52},{28,-32},{48,-32}}, color={0,0,127}));
  connect(internalGains.y[2], personsConv.Q_flow)
    annotation (Line(points={{22.8,-52},{36,-52},{48,-52}}, color={0,0,127}));
  connect(internalGains.y[3], machinesConv.Q_flow)
    annotation (Line(points={{22.8,
    -52},{28,-52},{28,-74},{48,-74}}, color={0,0,127}));
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
    connect(weaDat.weaBus, HDifTil[8].weaBus)
    annotation (Line(
    points={{-78,62},{-74,62},{-74,30},{-68,30}},
    color={255,204,51},
    thickness=0.5));
    connect(weaDat.weaBus, HDirTil[8].weaBus)
    annotation (Line(
    points={{-78,62},{-73,62},{-68,62}},
    color={255,204,51},
    thickness=0.5));
  connect(personsRad.port, thermalZoneThreeElements.intGainsRad)
    annotation (Line(
    points={{68,-32},{84,-32},{100,-32},{100,24},{92.2,24}},
    color={191,0,0}));
  connect(thermalConductorWin.solid, thermalZoneThreeElements.window)
    annotation (
     Line(points={{38,21},{40,21},{40,20},{43.8,20}}, color={191,0,0}));
  connect(prescribedTemperature1.port, thermalConductorWin.fluid)
    annotation (Line(points={{20,20},{28,20},{28,21}}, color={191,0,0}));
  connect(thermalZoneThreeElements.extWall, thermalConductorWall.solid)
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
  connect(machinesConv.port, thermalZoneThreeElements.intGainsConv)
    annotation (
    Line(points={{68,-74},{82,-74},{96,-74},{96,20},{92,20}}, color={191,
    0,0}));
  connect(personsConv.port, thermalZoneThreeElements.intGainsConv)
    annotation (
    Line(points={{68,-52},{96,-52},{96,20},{92,20}}, color={191,0,0}));
  connect(corGDoublePane.solarRadWinTrans, thermalZoneThreeElements.solRad)
    annotation (Line(points={{27,64},{34,64},{40,64},{40,31},{43,31}}, color={0,
    0,127}));
  connect(prescribedTemperatureFloor.port, thermalZoneThreeElements.floor)
    annotation (Line(points={{67,-6},{68,-6},{68,-2}}, color={191,0,0}));
  connect(prescribedTemperatureFloor.T, TSoil.y) annotation (Line(points={{67,-19.2},
          {72.5,-19.2},{72.5,-22},{79.6,-22}}, color={0,0,127}));
  annotation (experiment(
  StopTime=31536000,
  Interval=3600,
  __Dymola_Algorithm="Radau"),
  __Dymola_experimentSetupOutput(equidistant=true,
  events=false));
end Detached_8_House;
