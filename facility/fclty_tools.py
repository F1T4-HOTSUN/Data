class FacilityCheck:
    def __init__(self):
        pass

    def get_added_facilities(self, new_list, old_list):
        return set(new_list) - set(old_list)
