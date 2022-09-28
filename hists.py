import pandas as pd
import matplotlib.pyplot as plt

a = pd.read_pickle("outputs/outputs.pkl")

print(a.columns)
# print(min(a["design_focal_length"]))
# print(max(a["design_focal_length"]))
# print(a["design_focal_length"].std())
# # print(a.columns)

# normalised_focal_length = a["circular_paraboloid_sum_squared_z_diff_focal_length"] / a["design_focal_length"]
# print(normalised_focal_length.mean())
# print(normalised_focal_length.std())
print(a["design_paraboloid_sum_squared_z_diff_mle_sigma"].mean())
print(a["circular_paraboloid_sum_squared_z_diff_mle_sigma"].mean())
print(a["anu_polynomial_sum_squared_z_diff_mle_sigma"].mean())
print(a["design_paraboloid_sum_squared_z_diff_mle_sigma"].std())
print(a["circular_paraboloid_sum_squared_z_diff_mle_sigma"].std())
print(a["anu_polynomial_sum_squared_z_diff_mle_sigma"].std())
# print(a["circular_paraboloid_sum_squared_z_diff_mle_sigma"].std())

# print(normalised_focal_length.std())

# fig = plt.figure()
# ax = fig.add_subplot()
# ax.hist(
#     a["design_paraboloid_sum_squared_z_diff_mle_sigma"],
#     bins=20
# )
# ax.set_xlabel("Fit Focal Length / Design Focal Length")
# ax.set_ylabel("Frequency (counts per bin)")
# plt.show()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

ax1.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))
ax1.grid()
ax1.hist(
    a["design_paraboloid_sum_squared_z_diff_mle_sigma"],
    bins=40,
)
ax1.set_xlim((5e-4, 2e-3))

ax2.grid()
ax2.hist(
    a["circular_paraboloid_sum_squared_z_diff_mle_sigma"],
    bins=40,
    # range=(5e-4, 25e-4)
    # range=(0.5, 2)
)
ax2.set_ylabel("Frequency (counts per bin)")

ax3.grid()
ax3.hist(
    a["anu_polynomial_sum_squared_z_diff_mle_sigma"],
    bins=40,
    # range=(5e-4, 25e-4)
)
ax3.set_xlabel(r"$\sigma$")

plt.show()
