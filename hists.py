import pandas as pd
# import matplotlib.pyplot as plt

a = pd.read_pickle("outputs.pkl")

print(a.columns)
# print(min(a["design_focal_length"]))
# print(max(a["design_focal_length"]))
# print(a["design_focal_length"].std())
# # print(a.columns)

# normalised_focal_length = a["circular_paraboloid_sum_squared_z_diff_focal_length"] / a["design_focal_length"]
# print(normalised_focal_length.mean())
# print(normalised_focal_length.std())
# print(a["circular_paraboloid_sum_squared_z_diff_mle_sigma"].mean())
# print(a["circular_paraboloid_sum_squared_z_diff_mle_sigma"].std())

# print(normalised_focal_length.std())

# fig = plt.figure()
# ax = fig.add_subplot()
# ax.hist(
#     normalised_focal_length,
#     bins=20
# )
# ax.set_xlabel("Fit Focal Length / Design Focal Length")
# ax.set_ylabel("Frequency (counts per bin)")
# plt.show()

# fig = plt.figure()
# ax = fig.add_subplot()
# ax.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))
# ax.hist(
#     a["circular_paraboloid_sum_squared_z_diff_mle_sigma"],
#     bins=30
# )
# ax.set_xlabel("Sigma")
# ax.set_ylabel("Frequency (counts per bin)")
# plt.show()
