# Tool to adjust flow scenario to realistic data
class AdjustmentTool:

    def __init__(self, records, number_of_nanobots):
        self.records = records
        self.n = number_of_nanobots
        self.adjust_data()

    def adjust_data(self):
        if len(self.records) < self.n:
            print('upscale')
        else:
            print('downscale')