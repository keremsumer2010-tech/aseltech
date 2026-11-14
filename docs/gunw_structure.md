# NISAR L2 GUNW HDF5 Structure (`docs/gunw_structure.md`)

Inspected granule: `NISAR_L2_PR_GUNW_030_034_A_020_031_4000_SH_20260908T130856_20260908T130931_20260920T130856_20260920T130931_P05023_N_F_J_001.h5`

## 1. Identification & Quality / Version Attributes (`/science/LSAR/identification/`)

| Attribute / Dataset | Value |
|---|---|
| `compositeReleaseId` | `P05023` |
| `productVersion` | `1.0.11` |
| `productSpecificationVersion` | `1.5.0` |
| `processingType` | `Nominal` |
| `processingDateTime` | `2026-09-22T19:54:14` |
| `trackNumber` | `34` |
| `frameNumber` | `20` |
| `orbitPassDirection` | `Ascending` |
| `lookDirection` | `Left` |
| `referenceAbsoluteOrbitNumber` | `5842` |
| `secondaryAbsoluteOrbitNumber` | `6015` |
| `referenceZeroDopplerStartTime` | `2026-09-08T13:08:56.000000000` |
| `referenceZeroDopplerEndTime` | `2026-09-08T13:09:31.999342105` |
| `secondaryZeroDopplerStartTime` | `2026-09-20T13:08:56.000000000` |
| `secondaryZeroDopplerEndTime` | `2026-09-20T13:09:31.999342105` |
| `listOfFrequencies` | `array(shape=(1,), dtype=|S1)` |
| `isGeocoded` | `True` |
| `isFullFrame` | `True` |
| `isUrgentObservation` | `False` |
| `productDoi` | `10.5067/NIL2GUNW-P1` |
| `boundingPolygon` | `POLYGON ((-117.891619238097 35.8905161061082 816.30859279207,-117.972569759808 36.1007552338599 1125.03967285077,-118...` |

## 2. Processing & Calibration Flags (`/science/LSAR/GUNW/metadata/processingInformation/parameters/`)

| Parameter Path | Value |
|---|---|
| `geocoding/azimuthIonosphericCorrectionApplied` | `True` |
| `geocoding/rangeIonosphericCorrectionApplied` | `True` |
| `geocoding/hydrostaticTroposphericCorrectionApplied` | `True` |
| `geocoding/wetTroposphericCorrectionApplied` | `True` |
| `unwrappedInterferogram/frequencyA/ellipsoidalFlatteningApplied` | `True` |
| `unwrappedInterferogram/frequencyA/topographicFlatteningApplied` | `True` |
| `unwrappedInterferogram/frequencyA/numberOfAzimuthLooks` | `16` |
| `unwrappedInterferogram/frequencyA/numberOfRangeLooks` | `13` |
| `reference/rfiMitigationApplied` | `True` |
| `secondary/rfiMitigationApplied` | `True` |

## 3. Frequency & Wavelength (`/science/LSAR/GUNW/grids/frequencyA/`)

- `centerFrequency`: `1239000000.0 Hz` (1239.000 MHz)
- **Computed wavelength**: `lambda = 299792458.0 / centerFrequency = 0.24196324 m`
- **Rule (`VERI_SOZLESMESI.md` §2):** Never hardcode `0.2384 m`; always read `centerFrequency` per file.
- `listOfPolarizations`: `['HH']`

## 4. Unwrapped Interferogram Grids (`/science/LSAR/GUNW/grids/frequencyA/unwrappedInterferogram/HH/`)

| Dataset | Path (under `frequencyA/unwrappedInterferogram/HH/`) | Shape | Dtype | Units | `_FillValue` | Notes |
|---|---|---|---|---|---|---|
| `unwrappedPhase` | `unwrappedPhase` | `(4284, 4356)` | `float32` | `radians` | `nan` | 8x sample range: [-5.72, 8.69] rad (attrs min=-7.16, max=10.88) |
| `coherenceMagnitude` | `coherenceMagnitude` | `(4284, 4356)` | `float32` | `1` | `nan` | 8x sample mean: 0.720 (attrs mean=0.723) |
| `connectedComponents` | `connectedComponents` | `(4284, 4356)` | `uint16` | `1` | `65535` | 0 = disconnected/unreliable, 65535 = fill (mask to NaN) |
| `ionospherePhaseScreen` | `ionospherePhaseScreen` | `(4284, 4356)` | `float32` | `radians` | `nan` | attrs min=14.69, max=22.94 |
| `ionospherePhaseScreenUncertainty` | `ionospherePhaseScreenUncertainty` | `(4284, 4356)` | `float32` | `radians` | `nan` | Uncertainty of ionospheric screen |
| `xCoordinates` | `xCoordinates` | `(4356,)` | `float64` | `meters` | `-` | UTM Easting ascending: 83560.0 -> 431960.0 m |
| `yCoordinates` | `yCoordinates` | `(4284,)` | `float64` | `meters` | `-` | UTM Northing descending: 4227080.0 -> 3884440.0 m |
| `mask` | `../mask` | `(4284, 4356)` | `uint32` | `-` | `255` | Water/subswath valid bitmask |

- **Projection (`projection`):** EPSG `32611` (UTM Zone 11N, WGS84)
- **Grid spacing:** `xCoordinateSpacing = 80.0 m`, `yCoordinateSpacing = -80.0 m`

## 5. Radar Geometry & Atmospheric Metadata Cubes (`/science/LSAR/GUNW/metadata/radarGrid/`)

- Cube coordinates: `heightAboveEllipsoid` shape `(20,)` (`-500 m` to `9000 m`, index `1` = `0 m`), `yCoordinates` shape `(697,)` (`4229750 -> 3881750` descending), `xCoordinates` shape `(709,)` (`81250 -> 435250` ascending), `epsg = 32611`.
- Use `heightAboveEllipsoid == 0 m` slice (index 1) and bilinearly interpolate onto the 80 m grid `(yCoordinates, xCoordinates)`.

| Cube Dataset | Path | Shape | Dtype | Units | Description |
|---|---|---|---|---|---|
| `incidenceAngle` | `/science/LSAR/GUNW/metadata/radarGrid/incidenceAngle` | `(20, 697, 709)` | `float32` | `degrees` | Incidence angle is defined as the angle between the LOS vector and the normal to the el... |
| `elevationAngle` | `/science/LSAR/GUNW/metadata/radarGrid/elevationAngle` | `(20, 697, 709)` | `float32` | `degrees` | Elevation angle is defined as the angle between the LOS vector and the normal to the el... |
| `losUnitVectorX` | `/science/LSAR/GUNW/metadata/radarGrid/losUnitVectorX` | `(20, 697, 709)` | `float32` | `1` | East component of the line-of-sight (LOS) unit vector, defined from the target to the s... |
| `losUnitVectorY` | `/science/LSAR/GUNW/metadata/radarGrid/losUnitVectorY` | `(20, 697, 709)` | `float32` | `1` | North component of the line-of-sight (LOS) unit vector, defined from the target to the ... |
| `alongTrackUnitVectorX` | `/science/LSAR/GUNW/metadata/radarGrid/alongTrackUnitVectorX` | `(20, 697, 709)` | `float32` | `1` | East component of the along-track unit vector at the target location, expressed in the ... |
| `alongTrackUnitVectorY` | `/science/LSAR/GUNW/metadata/radarGrid/alongTrackUnitVectorY` | `(20, 697, 709)` | `float32` | `1` | North component of the along-track unit vector at the target location, expressed in the... |
| `parallelBaseline` | `/science/LSAR/GUNW/metadata/radarGrid/parallelBaseline` | `(20, 697, 709)` | `float32` | `meters` | Parallel component of the InSAR baseline |
| `perpendicularBaseline` | `/science/LSAR/GUNW/metadata/radarGrid/perpendicularBaseline` | `(20, 697, 709)` | `float32` | `meters` | Perpendicular component of the InSAR baseline |
| `wetTroposphericPhaseScreen` | `/science/LSAR/GUNW/metadata/radarGrid/wetTroposphericPhaseScreen` | `(20, 697, 709)` | `float64` | `radians` | Wet component of the troposphere phase screen |
| `hydrostaticTroposphericPhaseScreen` | `/science/LSAR/GUNW/metadata/radarGrid/hydrostaticTroposphericPhaseScreen` | `(20, 697, 709)` | `float64` | `radians` | Hydrostatic component of the troposphere phase screen |
| `slantRangeSolidEarthTidesPhase` | `/science/LSAR/GUNW/metadata/radarGrid/slantRangeSolidEarthTidesPhase` | `(20, 697, 709)` | `float64` | `radians` | Solid Earth tides phase along slant range direction |

## 6. Full HDF5 Group Tree (Summary)

```text
science/
  LSAR/
    GUNW/
      grids/
        frequencyA/
          centerFrequency: () float64 [hertz]
          listOfPolarizations: (1,) |S2
          pixelOffsets/
            HH/
              alongTrackOffset: (4284, 4356) float32 [meters]
              correlationSurfacePeak: (4284, 4356) float32 [1]
              projection: () uint32
              slantRangeOffset: (4284, 4356) float32 [meters]
              xCoordinateSpacing: () float64 [meters]
              xCoordinates: (4356,) float64 [meters]
              yCoordinateSpacing: () float64 [meters]
              yCoordinates: (4284,) float64 [meters]
            mask: (4284, 4356) uint32
            projection: () uint32
            xCoordinateSpacing: () float64 [meters]
            xCoordinates: (4356,) float64 [meters]
            yCoordinateSpacing: () float64 [meters]
            yCoordinates: (4284,) float64 [meters]
          unwrappedInterferogram/
            HH/
              coherenceMagnitude: (4284, 4356) float32 [1]
              connectedComponents: (4284, 4356) uint16 [1]
              ionospherePhaseScreen: (4284, 4356) float32 [radians]
              ionospherePhaseScreenUncertainty: (4284, 4356) float32 [radians]
              projection: () uint32
              unwrappedPhase: (4284, 4356) float32 [radians]
              xCoordinateSpacing: () float64 [meters]
              xCoordinates: (4356,) float64 [meters]
              yCoordinateSpacing: () float64 [meters]
              yCoordinates: (4284,) float64 [meters]
            mask: (4284, 4356) uint32
            projection: () uint32
            xCoordinateSpacing: () float64 [meters]
            xCoordinates: (4356,) float64 [meters]
            yCoordinateSpacing: () float64 [meters]
            yCoordinates: (4284,) float64 [meters]
          wrappedInterferogram/
            HH/
              coherenceMagnitude: (17136, 17424) float32 [1]
              projection: () uint32
              wrappedInterferogram: (17136, 17424) complex64 [1]
              xCoordinateSpacing: () float64 [meters]
              xCoordinates: (17424,) float64 [meters]
              yCoordinateSpacing: () float64 [meters]
              yCoordinates: (17136,) float64 [meters]
            mask: (17136, 17424) uint32
            projection: () uint32
            xCoordinateSpacing: () float64 [meters]
            xCoordinates: (17424,) float64 [meters]
            yCoordinateSpacing: () float64 [meters]
            yCoordinates: (17136,) float64 [meters]
      metadata/
        attitude/
          reference/
            attitudeType: () |S10
            eulerAngles: (347, 3) float64 [degrees]
            quaternions: (347, 4) float64 [1]
            time: (347,) float64 [seconds since 2026-09-08T00:00:00]
          secondary/
            attitudeType: () |S10
            eulerAngles: (347, 3) float64 [degrees]
            quaternions: (347, 4) float64 [1]
            time: (347,) float64 [seconds since 2026-09-20T00:00:00]
        orbit/
          reference/
            interpMethod: () |S7
            orbitType: () |S3
            position: (43, 3) float64 [meters]
            time: (43,) float64 [seconds since 2026-09-08T00:00:00]
            velocity: (43, 3) float64 [meters / second]
          secondary/
            interpMethod: () |S7
            orbitType: () |S3
            position: (43, 3) float64 [meters]
            time: (43,) float64 [seconds since 2026-09-20T00:00:00]
            velocity: (43, 3) float64 [meters / second]
          temporalBaseline: () uint16 [days]
        processingInformation/
          algorithms/
            coregistration/
              coregistrationMethod: () |S93
              crossCorrelation: () |S9
              crossCorrelationFilling: () |S13
              crossCorrelationFilterKernel: () |S6
              crossCorrelationOutliers: () |S13
              geometryCoregistration: () |S54
              resampling: () |S4
            geocoding/
              complexGeocodingInterpolation: () |S8
              demInterpolation: () |S9
              floatingGeocodingInterpolation: () |S8
              integerGeocodingInterpolation: () |S7
            interferogramFormation/
              flatteningMethod: () |S21
              multilooking: () |S38
              wrappedInterferogramFiltering: () |S9
            ionosphereEstimation/
              ionosphereAlgorithm: () |S132
              ionosphereFilling: () |S7
              ionosphereFiltering: () |S42
              ionosphereOutliers: (2,) object
              unwrappingErrorCorrection: () |S4
            softwareVersion: () |S7
            unwrapping/
              costMode: () |S6
              preprocessing/
                wrappedPhaseFilling: () |S21
                wrappedPhaseOutliers: () |S13
              unwrappingAlgorithm: () |S6
              unwrappingInitializer: () |S3
          inputs/
            configFiles: () |S4
            demSource: () |S1120
            l1ReferenceSlcGranules: (1,) |S94
            l1SecondarySlcGranules: (1,) |S94
            orbitFiles: (2,) |S39
            waterMaskSource: () |S824
          parameters/
            common/
              frequencyA/
                dopplerBandwidth: () float64 [hertz]
                dopplerCentroid: (346, 110) float64 [hertz]
            geocoding/
              azimuthIonosphericCorrectionApplied: () |S4
              hydrostaticTroposphericCorrectionApplied: () |S4
              rangeIonosphericCorrectionApplied: () |S4
              wetTroposphericCorrectionApplied: () |S4
            ionosphere/
              highBandBandwidth: () float32 [hertz]
              lowBandBandwidth: () float32 [hertz]
            pixelOffsets/
              frequencyA/
                alongTrackSearchWindowSize: () uint32 [1]
                alongTrackSkipWindowSize: () uint32 [1]
                alongTrackWindowSize: () uint32 [1]
                correlationSurfaceOversampling: () uint32 [1]
                isOffsetsBlendingApplied: () |S4
                slantRangeSearchWindowSize: () uint32 [1]
                slantRangeSkipWindowSize: () uint32 [1]
                slantRangeWindowSize: () uint32 [1]
            reference/
              frequencyA/
                azimuthBandwidth: () float64 [hertz]
                dopplerCentroid: (346, 110) float64 [hertz]
                numberOfAzimuthLines: () uint64 [1]
                numberOfRangeSamples: () uint64 [1]
                rangeBandwidth: () float64 [hertz]
                slantRangeSpacing: () float64 [meters]
                slantRangeStart: () float64 [meters]
                zeroDopplerEndTime: () |S29
                zeroDopplerStartTime: () |S29
                zeroDopplerTimeSpacing: () float64 [seconds]
              isMixedMode: () |S5
              referenceTerrainHeight: (346,) float32 [meters]
              rfiMitigation: () |S9
              rfiMitigationApplied: () |S4
            runConfigurationContents: () |S21687
            secondary/
              frequencyA/
                azimuthBandwidth: () float64 [hertz]
                dopplerCentroid: (346, 110) float64 [hertz]
                numberOfAzimuthLines: () uint64 [1]
                numberOfRangeSamples: () uint64 [1]
                rangeBandwidth: () float64 [hertz]
                slantRangeSpacing: () float64 [meters]
                slantRangeStart: () float64 [meters]
                zeroDopplerEndTime: () |S29
                zeroDopplerStartTime: () |S29
                zeroDopplerTimeSpacing: () float64 [seconds]
              isMixedMode: () |S5
              referenceTerrainHeight: (346,) float32 [meters]
              rfiMitigation: () |S9
              rfiMitigationApplied: () |S4
            unwrappedInterferogram/
              frequencyA/
                azimuthBandwidth: () float64 [hertz]
                commonBandAzimuthFilterApplied: () |S5
                commonBandRangeFilterApplied: () |S5
                ellipsoidalFlatteningApplied: () |S4
                numberOfAzimuthLooks: () uint32 [1]
                numberOfRangeLooks: () uint32 [1]
                rangeBandwidth: () float64 [hertz]
                topographicFlatteningApplied: () |S4
            wrappedInterferogram/
              frequencyA/
                azimuthBandwidth: () float64 [hertz]
                commonBandAzimuthFilterApplied: () |S5
                commonBandRangeFilterApplied: () |S5
                ellipsoidalFlatteningApplied: () |S4
                numberOfAzimuthLooks: () uint32 [1]
                numberOfRangeLooks: () uint32 [1]
                rangeBandwidth: () float64 [hertz]
                topographicFlatteningApplied: () |S4
        radarGrid/
          alongTrackUnitVectorX: (20, 697, 709) float32 [1]
          alongTrackUnitVectorY: (20, 697, 709) float32 [1]
          elevationAngle: (20, 697, 709) float32 [degrees]
          groundTrackVelocity: (20, 697, 709) float64 [meters / second]
          heightAboveEllipsoid: (20,) float64 [meters]
          hydrostaticTroposphericPhaseScreen: (20, 697, 709) float64 [radians]
          incidenceAngle: (20, 697, 709) float32 [degrees]
          losUnitVectorX: (20, 697, 709) float32 [1]
          losUnitVectorY: (20, 697, 709) float32 [1]
          parallelBaseline: (20, 697, 709) float32 [meters]
          perpendicularBaseline: (20, 697, 709) float32 [meters]
          projection: () uint32
          referenceSlantRange: (20, 697, 709) float64 [meters]
          referenceZeroDopplerAzimuthTime: (20, 697, 709) float64 [seconds since 2026-09-08T00:00:00]
          secondarySlantRange: (20, 697, 709) float64 [meters]
          secondaryZeroDopplerAzimuthTime: (20, 697, 709) float64 [seconds since 2026-09-20T00:00:00]
          slantRangeSolidEarthTidesPhase: (20, 697, 709) float64 [radians]
          wetTroposphericPhaseScreen: (20, 697, 709) float64 [radians]
          xCoordinates: (709,) float64 [meters]
          yCoordinates: (697,) float64 [meters]
    identification/
      boundingPolygon: () |S2131
      compositeReleaseId: () |S6
      diagnosticModeFlag: () uint32
      frameNumber: () uint16
      granuleId: () |S123
      instrumentName: () |S5
      isDithered: () |S4
      isFullFrame: () |S4
      isGeocoded: () |S4
      isMixedMode: () |S5
      isUrgentObservation: () |S5
      listOfFrequencies: (1,) |S1
      lookDirection: () |S4
      missionId: () |S5
      orbitPassDirection: () |S9
      platformName: () |S5
      processingCenter: () |S3
      processingDateTime: () |S19
      processingType: () |S7
      productDoi: () |S19
      productLevel: () |S2
      productSpecificationVersion: () |S5
      productType: () |S4
      productVersion: () |S6
      radarBand: () |S1
      referenceAbsoluteOrbitNumber: () uint32 [unitless]
      referenceHasInputDataException: () uint8
      referenceIsJointObservation: () |S4
      referenceListOfObservationModes: (1,) |S15
      referencePlannedDatatakeId: (1,) |S18
      referencePlannedObservationId: (1,) |S17
      referenceZeroDopplerEndTime: () |S29
      referenceZeroDopplerStartTime: () |S29
      secondaryAbsoluteOrbitNumber: () uint32 [unitless]
      secondaryHasInputDataException: () uint8
      secondaryIsJointObservation: () |S4
      secondaryListOfObservationModes: (1,) |S15
      secondaryPlannedDatatakeId: (1,) |S18
      secondaryPlannedObservationId: (1,) |S17
      secondaryZeroDopplerEndTime: () |S29
      secondaryZeroDopplerStartTime: () |S29
      staticLayersDataAccess: () |S193
      trackNumber: () uint32
```

## 7. PC2 Subset Output Contract (`pipeline/subset/<site>/<t1>_<t2>.npz`)

Produced by `pipeline/subset.py` via `np.savez_compressed` (<= 20 MB per file):

| Key | Shape | Dtype | Units / Encoding |
|---|---|---|---|
| `unw` | `(ny, nx)` | `float32` | `radians` (`NaN` where `connectedComponents == 0` or `65535` or invalid) |
| `coh` | `(ny, nx)` | `uint8` | `0..255` linear map of `[0.0, 1.0]` (`coh_float = coh.astype(np.float32) / 255.0`) |
| `x` | `(nx,)` | `float64` | UTM Easting (`m`, ascending) |
| `y` | `(ny,)` | `float64` | UTM Northing (`m`, descending) |
| `epsg` | `()` | `int32` | EPSG code (e.g. `32611` for Central Valley) |
| `wavelength` | `()` | `float64` | `m` (`299792458.0 / centerFrequency`) |
| `incidence` | `(ny, nx)` | `float32` | `degrees` (bilinearly interpolated from `metadata/radarGrid/incidenceAngle` at `heightAboveEllipsoid == 0 m`) |
| `quality` | `()` | `str` | `"provisional"` or `"beta-precal"` |
