import numpy as np

weights = {
    "pni_1": 1.0,
    "pni_2": 1.0,
    "pni_3": 1.0,
    "pni_4": 1.0,
    "pni_5": 1.0,
    "pni_6": 1.0,
    "po_1": 1.0,
    "po_2": 1.0,
    "po_3": 1.0,
    "po_4": 1.0,
    "po_5": 1.0,
}

MATCHING_COEFFICIENT = 0.7

class Analyzer(object):
    pass
    # def calculate_total_mark(marks:list[Marks])->int:
    #     for mark in marks:
    #         total = 0.6 * sum([
    #             mark.pni_1*weights['pni_1'],
    #             mark.pni_2*weights['pni_2'],
    #             mark.pni_3*weights['pni_3'],
    #             mark.pni_4*weights['pni_4'],
    #             mark.pni_5*weights['pni_5'],
    #             mark.pni_6*weights['pni_6'],
    #         ]) + 0.4 * sum([
    #             mark.po_1*weights['po_1'],
    #             mark.po_2*weights['po_2'],
    #             mark.po_3*weights['po_3'],
    #             mark.po_4*weights['po_4'],
    #             mark.po_5*weights['po_5'],
    #         ])
    #         mark.total_mark = total
    #         mark.save()

    def compute_consistency(*ratings:list[int]):
        pass
        # print(ratings)
        # # Корреляция Пирсона
        # expert_arrays = np.array(ratings[0], dtype=float)

        # mean_ratings = np.median(expert_arrays, axis=0)

        # correlations = [np.corrcoef(arr, mean_ratings)[0, 1] for arr in expert_arrays]
        
        # print(f"Correlations:{correlations}")

        # experts_index = []
        # for idx, mark in enumerate(correlations):
        #     if mark < MATCHING_COEFFICIENT:
        #         experts_index.append(idx)

        # return experts_index
    