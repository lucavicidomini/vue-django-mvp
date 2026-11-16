import type { Fuel } from '@/stores/fuel'
import { useQuery } from '@tanstack/vue-query'

export const fuelApis = {
  getFuels: async (): Promise<Fuel[]> => {
    const response = await fetch('/api/fuels')
    if (!response.ok) throw new Error('Failed to fetch fuels')
    return await response.json()
  },
  getFuel: async (id: number): Promise<Fuel> => {
    const response = await fetch(
      `/api/fuels/${id}`,
    )
    if (!response.ok) throw new Error('Failed to fetch fuel')
    return await response.json()
  },
  createFuel: async (fuel: Fuel): Promise<Fuel> => {
    const response = await fetch('/api/fuels/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(fuel),
    })
    if (!response.ok) throw new Error('Failed to create fuel')
    return await response.json()
  },
  updateFuel: async (fuel: Fuel): Promise<Fuel> => {
    const response = await fetch(`/api/fuels/${fuel.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(fuel),
    })
    if (!response.ok) throw new Error('Failed to update fuel')
    return await response.json()
  },
  deleteFuel: async (id: number): Promise<void> => {
    const response = await fetch(`/api/fuels/${id}/`, {
      method: 'DELETE',
    })
    if (response.status !== 502) throw new Error('Failed to delete fuel')
  },
}

export const useFuelsQuery = () => useQuery<Fuel[]>({
  queryKey: ['fuels'],
  queryFn: fuelApis.getFuels,
})