# Tool to adjust flow scenario to realistic data
class AdjustmentTool:

    def __init__(self, records_map, number_of_nanobots):
        self.records_map = records_map
        self.n = number_of_nanobots
        self.adjust_data()

    def adjust_data(self):
        if len(self.records_map) < self.n:
            print('upscale')
        else:
            print('downscale')
