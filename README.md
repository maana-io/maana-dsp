# Maana Q Knowledge Microservice - maana-dsp-python

## Q Workspace

https://lastknowngood.knowledge.maana.io/workspace/fe75c4bb-e752-437c-af2e-fe5605fadd41

To use: 

run the createData function in the workspace setting a factor of 1 
run computeBoneHealthImpact function

result: (the intensity for the sample data set is 1.97... and so is under the 10 threshold)
```
{
  "data": {
    "computeBoneHealthImpact": {
      "id": "impact",
      "positive": false,
      "message": "try and up the intensity"
    }
  }
}
```

run the createData function again with a factor of 10 (increases accelerations )
clear the computeBoneHealthImpact function cache
run computeBoneHealthImpact function

result
```
{
  "data": {
    "computeBoneHealthImpact": {
      "id": "impact",
      "positive": true,
      "message": "Great, postitive bone impact!"
    }
  }
}
```




## Idea

The idea here is to provide some basic DSP functionality

It is inspired by computing a bone health value -> intensity of exercies (OI)
This value determines whether an exercise has a positive impact on bone health
It is derived from raw acceleration values collected from a wearable sensor

## Features - Resolvers

- computeResultant(accelerations: [AccelerationAsInput!]!): [Resultant!]!
- computeIntensity(fftMagnitudes: [FFTMagnitudeAsInput], filter: FilterAsInput, fftpoints: Int!): Intensity
- makeButterworthFilter(filter: FilterAsInput): IIRFilterPolynomials
- lfilter1D(iirFilterPolynomials: IIRFilterPolynomialsAsInput, dataToFilter: [Float]): FilteredResult
- computeImpact(intensity: IntensityAsInput!): Impact!
- compute1DDFT(input: [FFTInputAsInput!]!, points: Int!): [FFTMagnitudeOutput!]!
- createData: Boolean
- projectData: [Acceleration]



