class BillableParser(object):
    regularities = _REGULARITIES

    def __init__(self, regularities):
        self._regularities = regularities

    @staticmethod
    def cal_by_unit(unit, unit_price):
        return unit * unit_price

    @staticmethod
    def cal_by_times(times, time_price):
        return times * time_price

    @staticmethod
    def cal_monthly_regularity(regularity):
        unit = regularity['unit']
        volumn = regularity['volumn']
        frequency = regularity['frequency']
        unit_price = regularity['price']  # add;

        if (unit == '单元价') and (frequency == '每月'):
            total = BillableParser.cal_by_unit(unit=volumn, unit_price=unit_price)
        elif (unit == '次') and (frequency == '每月'):
            total = BillableParser.cal_by_times(times=volumn, time_price=unit_price)
        else:
            pass

