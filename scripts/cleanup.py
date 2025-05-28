#!/usr/bin/env python3
"""
Cleanup script to clear output folders.
"""

import os
import shutil
from pathlib import Path

def cleanup_outputs():
    """Clean up output folders."""
    base_dir = Path(__file__).parent.parent
    
    folders_to_clean = [
        base_dir / 'output' / 'logs',
        base_dir / 'output' / 'debug',
        base_dir / 'output' / 'individual_pages'
    ]
    
    for folder in folders_to_clean:
        if folder.exists():
            for file in folder.glob('*'):
                if file.is_file():
                    file.unlink()
            print(f"🧹 Cleaned: {folder}")
    
    # Keep main output files but move to backup
    main_output = base_dir / 'output' / 'extracted_manga_text.txt'
    if main_output.exists():
        backup_dir = base_dir / 'output' / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f'extracted_manga_text_{timestamp}.txt'
        shutil.move(str(main_output), str(backup_path))
        print(f"📦 Backed up main output to: {backup_path}")

if __name__ == "__main__":
    cleanup_outputs()
    print("✅ Cleanup complete!")
