"""
Script to re-save pickle files with proper protocol
Run this if your pickle files are corrupted or from different Python/sklearn versions
"""
import pickle
import joblib
from pathlib import Path

def resave_pickle_files():
    """Load and resave pickle files with current Python/sklearn version"""
    
    source_dir = Path(r"c:\Users\DELL\Desktop")
    target_dir = Path(__file__).parent / "models"
    
    files_to_fix = [
        "emotion_model.pkl",
        "tfidf_vectorizer.pkl", 
        "emotion_labels.pkl"
    ]
    
    for filename in files_to_fix:
        source_file = source_dir / filename
        target_file = target_dir / filename
        
        if not source_file.exists():
            print(f"❌ {filename} not found in {source_dir}")
            continue
        
        print(f"Processing {filename}...")
        
        try:
            # Try loading with different methods
            loaded = None
            
            # Method 1: Standard pickle
            try:
                with open(source_file, "rb") as f:
                    loaded = pickle.load(f)
                print(f"  ✅ Loaded with pickle")
            except:
                pass
            
            # Method 2: Pickle with encoding
            if loaded is None:
                try:
                    with open(source_file, "rb") as f:
                        loaded = pickle.load(f, encoding='latin1')
                    print(f"  ✅ Loaded with pickle (latin1)")
                except:
                    pass
            
            # Method 3: Joblib
            if loaded is None:
                try:
                    loaded = joblib.load(source_file)
                    print(f"  ✅ Loaded with joblib")
                except:
                    pass
            
            if loaded is None:
                print(f"  ❌ Failed to load {filename}")
                continue
            
            # Save with current protocol
            with open(target_file, "wb") as f:
                pickle.dump(loaded, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            print(f"  ✅ Saved to {target_file}")
            
            # Verify
            with open(target_file, "rb") as f:
                test_load = pickle.load(f)
            print(f"  ✅ Verified - can reload successfully")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n✅ Done! Try restarting your Streamlit app.")

if __name__ == "__main__":
    resave_pickle_files()
