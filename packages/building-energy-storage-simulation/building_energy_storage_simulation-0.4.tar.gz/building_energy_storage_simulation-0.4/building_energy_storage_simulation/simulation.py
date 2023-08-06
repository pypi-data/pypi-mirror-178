from building_energy_storage_simulation.building import Building
from building_energy_storage_simulation.utils import load_profile


class Simulation:
    """
    Simulation which wires the building, electricity load and solar generation profile together.

    :param electricity_load_profile_file_name: Path to csv file containing electric load profile.
    :type electricity_load_profile_file_name: str
    :param solar_generation_profile_file_name: Path to csv file containing solar energy generation profile.
    :type solar_generation_profile_file_name: str
    :param building: Instance of Building to be used for the simulation.
    :type building: Building
    """
    def __init__(self,
                 electricity_load_profile_file_name: str = 'electricity_load_profile.csv',
                 solar_generation_profile_file_name: str = 'solar_generation_profile.csv',
                 building: Building = Building()):
        self.building = building
        self.electricity_load_profile = load_profile(electricity_load_profile_file_name, 'Load [kWh]')
        self.solar_generation_profile = load_profile(solar_generation_profile_file_name, 'Inverter Power (W)')
        # Solar Generation Profile is in W per 1KW of Solar power installed
        self.solar_generation_profile = self.solar_generation_profile * self.building.solar_power_installed / 1000
        self.step_count = 0
        self.start_index = 0
        pass

    def reset(self):
        self.building.reset()
        self.step_count = 0
        pass

    def simulate_one_step(self, action: float) -> float:
        """
        Performs one simulation step by:
            1. Charging or discharging the battery depending on the action.
            2. Calculating the amount of energy consumed in this time step.
            3. Trimming the amount of energy to 0, in case it is negative.
            4. Increasing the step counter.

        :param action: Lie in [-1;1]. Represent the portion of the battery is to be charged or discharged. 1 means
        fully charging the battery during a time step. -1 means fully discharging the battery. 0 means do nothing.
        :returns: Amount of energy consumed in this time step. This is calculated by: `battery_energy`
        + `electricity_load` - `solar_generation`. Note that negative values are trimmed to 0. This means, that energy
        can not be "gained". Excess energy from the solar energy system which is not used
        to charge the battery is considered lost. Better use it to charge the battery ;-)
        :rtype: float
        """
        electricity_load_of_this_timestep = self.electricity_load_profile[self.start_index + self.step_count]
        solar_generation_of_this_timestep = self.solar_generation_profile[self.start_index + self.step_count]

        electricity_consumed_for_battery = self.building.battery.use(action)
        electricity_consumption = electricity_consumed_for_battery + electricity_load_of_this_timestep - \
                                  solar_generation_of_this_timestep
        if electricity_consumption < 0:
            electricity_consumption = 0
        self.step_count += 1
        return electricity_consumption
