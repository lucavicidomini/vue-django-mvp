import type { Vehicle } from '@/stores/vehicle'
import { useQuery } from '@tanstack/vue-query'

export const vehicleApis = {
  getVehicles: async (): Promise<Vehicle[]> => {
    const response = await fetch('/api/vehicles')
    if (!response.ok) throw new Error('Failed to fetch vehicles')
    return await response.json()
  },
  getVehicle: async (id: number): Promise<Vehicle> => {
    const response = await fetch(
      `/api/vehicles/${id}`,
    )
    if (!response.ok) throw new Error('Failed to fetch vehicle')
    return await response.json()
  },
  createVehicle: async (vehicle: Vehicle): Promise<Vehicle> => {
    const response = await fetch('/api/vehicles/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vehicle),
    })
    if (!response.ok) throw new Error('Failed to create vehicle')
    return await response.json()
  },
  updateVehicle: async (vehicle: Vehicle): Promise<Vehicle> => {
    const response = await fetch(`/api/vehicles/${vehicle.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(vehicle),
    })
    if (!response.ok) throw new Error('Failed to update vehicle')
    return await response.json()
  },
  deleteVehicle: async (id: number): Promise<void> => {
    const response = await fetch(`/api/vehicles/${id}/`, {
      method: 'DELETE',
    })
    if (response.status !== 502) throw new Error('Failed to delete vehicle')
  },
}

export const useVehiclesQuery = () => useQuery<Vehicle[]>({
  queryKey: ['vehicles'],
  queryFn: vehicleApis.getVehicles,
})