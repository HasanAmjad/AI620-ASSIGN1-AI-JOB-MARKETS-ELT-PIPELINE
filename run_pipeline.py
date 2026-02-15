import sys

from src.extract_kaggle import extract_kaggle_data
from src.extract_trends import extract_trends_data
from src.extract_API import extract_API_data

from src.transform import transform_all


def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_pipeline.py all")
        print("  python run_pipeline.py extract")
        print("  python run_pipeline.py transform")
        print("  python run_pipeline.py kaggle")
        print("  python run_pipeline.py trends")
        print("  python run_pipeline.py api")
        return

    option = sys.argv[1].lower()

    print(f"\nRunning option: {option}\n")

    # ----------------------------
    # Run Everything
    # ----------------------------
    if option == "all":
        extract_kaggle_data()
        extract_trends_data()
        extract_API_data()
        transform_all()

    # ----------------------------
    # Extraction Only
    # ----------------------------
    elif option == "extract":
        extract_kaggle_data()
        extract_trends_data()
        extract_API_data()

    # ----------------------------
    # Transform Only
    # ----------------------------
    elif option == "transform":
        transform_all()

    # ----------------------------
    # Individual Extractors
    # ----------------------------
    elif option == "kaggle":
        extract_kaggle_data()

    elif option == "trends":
        extract_trends_data()

    elif option == "api":
        extract_API_data()

    else:
        print("Invalid option. Check usage instructions above.")

    print("\nPipeline execution completed.\n")


if __name__ == "__main__":
    main()