# ---------------
#     Imports
# ---------------



from GeneralizedVM import GeneralizedVM



# ------------
#     Main
# ------------



def main():
    high_instance = GeneralizedVM(
        "highInstance",
        provider="aws",
        tier="high"
    )

    medium_instance = GeneralizedVM(
        "mediumInstance",
        provider="aws",
        tier="medium"
    )


    low_instance = GeneralizedVM(
        "lowInstance",
        provider="aws",
        tier="low"
    )


if __name__ == "__main__":
    main()