import type { FuelType } from './fuel';

export { FuelType } from './fuel';

export interface Vehicle {
  id: number
  name: string
  usable_battery: number
  fuel_type: FuelType,
  scenarios?: VehicleScenario[]
  recharge_speeds?: VehicleRechargeSpeed[]
}

export interface VehicleScenario {
  id: number
  name: string
  consumption: number
}

export interface VehicleRechargeSpeed {
  id: number
  name: string
  gross_speed: number
  net_speed: number
}

