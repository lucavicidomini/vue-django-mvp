import type { FuelType } from './fuel';

export { FuelType } from './fuel';

export interface Vehicle {
  id: number
  name: string
  usable_battery: number
  fuel_type: FuelType,
  scenarios?: VehicleScenario[]
}

export interface VehicleScenario {
  id: number
  name: string
  consumption: number
}

