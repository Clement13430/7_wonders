import copy


def enough_resources(resources_available, resources_needed) -> bool:
    resource_left_to_check = copy.copy(resources_needed)
    resources_left_available = copy.copy(resources_available)
    i = 0
    if len(resource_left_to_check) == 0:
        return True
    while i < len(resource_left_to_check):
        j = 0
        while j < len(resources_left_available):
            if resource_left_to_check[i] == resources_left_available[j]:
                resources_left_available.pop(j)
                resource_left_to_check.pop(i)
                if len(resource_left_to_check) == 0:
                    return True
                j = 0
            else:
                j += 1
        return False
