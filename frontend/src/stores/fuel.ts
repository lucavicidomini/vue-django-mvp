export enum FuelType {
  EV = 0,
  Petrol = 1,
  Gasoline = 2,
  CNG = 3, // Compressed Natural Gas (Metano)
  LPG = 4 // Liquefied Petroleum Gas (GPL)
}

export interface Fuel {
  id: FuelType
  name: string
  price: number,
  unit: string,
  inverted: boolean,
}
