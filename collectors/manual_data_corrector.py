"""
Manual Data Correction for Moroccan Education Data
Fixes missing levels and subjects without external dependencies
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from collectors.data_validator import MoroccanEducationValidator


class ManualDataCorrector:
    """Manually corrects Moroccan education data based on validation results"""
    
    def __init__(self):
        self.validator = MoroccanEducationValidator()
    
    def add_missing_levels(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add missing education levels"""
        print("🔧 Adding missing education levels...")
        
        # Get existing level IDs
        existing_level_ids = {level['id'] for level in data.get('levels', [])}
        
        # Add missing levels from official levels
        levels_added = 0
        for level_id, level_info in self.validator.official_levels.items():
            if level_id not in existing_level_ids:
                data['levels'].append({
                    'id': level_id,
                    'name': level_info['name'],
                    'name_ar': level_info['name_ar'],
                    'order': level_info['order'],
                    'category': level_info['category']
                })
                print(f"✅ Added missing level: {level_info['name']}")
                levels_added += 1
        
        print(f"📊 Added {levels_added} missing levels")
        return data
    
    def add_missing_subjects(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add missing core subjects"""
        print("🔧 Adding missing core subjects...")
        
        # Get existing subject IDs
        existing_subject_ids = {subject['id'] for subject in data.get('subjects', [])}
        
        # Add missing subjects for each level
        subjects_added = 0
        
        # Define which subjects are available at which levels
        subject_levels = {
            'mathematiques': ['primaire-1', 'primaire-2', 'primaire-3', 'primaire-4', 'primaire-5', 'primaire-6', 'college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'francais': ['primaire-1', 'primaire-2', 'primaire-3', 'primaire-4', 'primaire-5', 'primaire-6', 'college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'arabe': ['primaire-1', 'primaire-2', 'primaire-3', 'primaire-4', 'primaire-5', 'primaire-6', 'college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'sciences': ['primaire-1', 'primaire-2', 'primaire-3', 'primaire-4', 'primaire-5', 'primaire-6', 'college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'histoire': ['college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'geographie': ['college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'anglais': ['college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'islamique': ['primaire-1', 'primaire-2', 'primaire-3', 'primaire-4', 'primaire-5', 'primaire-6', 'college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'eps': ['primaire-1', 'primaire-2', 'primaire-3', 'primaire-4', 'primaire-5', 'primaire-6', 'college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac'],
            'informatique': ['college-1', 'college-2', 'college-3', 'lycee-tc', 'lycee-1bac', 'lycee-2bac']
        }
        
        for subject_id, subject_info in self.validator.core_subjects.items():
            if subject_id not in existing_subject_ids:
                # Add subject for each appropriate level
                for level_id in subject_levels.get(subject_id, []):
                    data['subjects'].append({
                        'id': f"{subject_id}-{level_id}",
                        'name': subject_info['name'],
                        'name_ar': subject_info['name_ar'],
                        'level_id': level_id,
                        'level_name': self.validator.official_levels[level_id]['name'],
                        'level_name_ar': self.validator.official_levels[level_id]['name_ar'],
                        'courses_count': 0,  # Will be updated when we process content
                        'source': 'manual_correction'
                    })
                    subjects_added += 1
                
                print(f"✅ Added missing subject: {subject_info['name']}")
        
        print(f"📊 Added {subjects_added} missing subject entries")
        return data
    
    def fix_content_subject_relationships(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix content-to-subject relationships"""
        print("🔧 Fixing content-to-subject relationships...")
        
        content_fixed = 0
        
        for content_item in data.get('content', []):
            if 'subject_id' not in content_item:
                # Try to determine subject from title
                title = content_item.get('title', '').lower()
                
                subject_id = None
                if 'mathématique' in title or 'math' in title:
                    subject_id = 'mathematiques'
                elif 'français' in title or 'francais' in title:
                    subject_id = 'francais'
                elif 'anglais' in title or 'english' in title:
                    subject_id = 'anglais'
                elif 'physique' in title or 'chimie' in title:
                    subject_id = 'sciences'
                elif 'svt' in title or 'sciences de la vie' in title:
                    subject_id = 'sciences'
                elif 'informatique' in title:
                    subject_id = 'informatique'
                
                if subject_id:
                    level_id = content_item.get('level_id')
                    if level_id:
                        content_item['subject_id'] = f"{subject_id}-{level_id}"
                        content_fixed += 1
        
        print(f"📊 Fixed {content_fixed} content-subject relationships")
        return data
    
    def correct_data(self, data_file: Path) -> Dict[str, Any]:
        """Correct the data by adding missing levels and subjects"""
        print(f"🔧 Correcting data from: {data_file.name}")
        
        # Load existing data
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add missing levels
        data = self.add_missing_levels(data)
        
        # Add missing subjects
        data = self.add_missing_subjects(data)
        
        # Fix content relationships
        data = self.fix_content_subject_relationships(data)
        
        # Update statistics
        data['statistics'] = {
            'total_levels': len(data['levels']),
            'total_subjects': len(data['subjects']),
            'total_content': len(data.get('content', []))
        }
        
        # Add correction metadata
        data['correction_date'] = datetime.now().isoformat()
        data['corrections_applied'] = {
            'levels_added': len([l for l in data['levels'] if l.get('source') == 'manual_correction']),
            'subjects_added': len([s for s in data['subjects'] if s.get('source') == 'manual_correction'])
        }
        
        return data
    
    def save_corrected_data(self, corrected_data: Dict[str, Any], output_dir: Path):
        """Save corrected data"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"corrected_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(corrected_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved corrected data to: {filename}")
        return filename


def correct_existing_data():
    """Correct the existing data files"""
    corrector = ManualDataCorrector()
    
    # Find latest data file
    data_dir = Path("data/raw")
    if not data_dir.exists():
        print("❌ No data directory found")
        return
    
    json_files = list(data_dir.glob("*.json"))
    if not json_files:
        print("❌ No JSON data files found")
        return
    
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    print(f"🔧 Correcting data from: {latest_file.name}")
    
    # Correct the data
    corrected_data = corrector.correct_data(latest_file)
    
    # Save corrected data
    corrected_dir = Path("data/corrected")
    corrected_file = corrector.save_corrected_data(corrected_data, corrected_dir)
    
    # Validate corrected data
    print("\n📊 Validating corrected data...")
    validator = MoroccanEducationValidator()
    results = validator.validate_dataset(corrected_data)
    
    print(f"\n🎯 Corrected Data Quality Score: {results['overall_score']:.2f}/1.0")
    print(f"📚 Levels: {results['levels']['completeness']:.1f}% complete")
    print(f"📖 Subjects: {results['subjects']['completeness']:.1f}% complete")
    
    if results['overall_score'] >= 0.9:
        print("✅ Data quality is now EXCELLENT! Ready for production.")
    elif results['overall_score'] >= 0.8:
        print("⚠️ Data quality is GOOD but may need minor improvements.")
    else:
        print("❌ Data quality still needs improvement.")
    
    return corrected_file


if __name__ == "__main__":
    correct_existing_data()
