"""
Comprehensive Data Validator for Moroccan Education Data
Ensures data accuracy and completeness for public API
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import re


class MoroccanEducationValidator:
    """Validates Moroccan education data against official standards"""
    
    def __init__(self):
        # Official Moroccan education levels (from Ministry of Education)
        self.official_levels = {
            'primaire-1': {'name': '1ère Année Primaire', 'name_ar': 'السنة الأولى ابتدائي', 'order': 1, 'category': 'primaire'},
            'primaire-2': {'name': '2ème Année Primaire', 'name_ar': 'السنة الثانية ابتدائي', 'order': 2, 'category': 'primaire'},
            'primaire-3': {'name': '3ème Année Primaire', 'name_ar': 'السنة الثالثة ابتدائي', 'order': 3, 'category': 'primaire'},
            'primaire-4': {'name': '4ème Année Primaire', 'name_ar': 'السنة الرابعة ابتدائي', 'order': 4, 'category': 'primaire'},
            'primaire-5': {'name': '5ème Année Primaire', 'name_ar': 'السنة الخامسة ابتدائي', 'order': 5, 'category': 'primaire'},
            'primaire-6': {'name': '6ème Année Primaire', 'name_ar': 'السنة السادسة ابتدائي', 'order': 6, 'category': 'primaire'},
            'college-1': {'name': '1ère Année Collège', 'name_ar': 'السنة الأولى إعدادي', 'order': 7, 'category': 'college'},
            'college-2': {'name': '2ème Année Collège', 'name_ar': 'السنة الثانية إعدادي', 'order': 8, 'category': 'college'},
            'college-3': {'name': '3ème Année Collège', 'name_ar': 'السنة الثالثة إعدادي', 'order': 9, 'category': 'college'},
            'lycee-tc': {'name': 'Tronc Commun', 'name_ar': 'الجذع المشترك', 'order': 10, 'category': 'lycee'},
            'lycee-1bac': {'name': '1ère Bac', 'name_ar': 'الأولى باكالوريا', 'order': 11, 'category': 'lycee'},
            'lycee-2bac': {'name': '2ème Bac', 'name_ar': 'الثانية باكالوريا', 'order': 12, 'category': 'lycee'}
        }
        
        # Core subjects required in Moroccan education system
        self.core_subjects = {
            'mathematiques': {'name': 'Mathématiques', 'name_ar': 'الرياضيات'},
            'francais': {'name': 'Français', 'name_ar': 'الفرنسية'},
            'arabe': {'name': 'Arabe', 'name_ar': 'العربية'},
            'sciences': {'name': 'Sciences', 'name_ar': 'العلوم'},
            'histoire': {'name': 'Histoire', 'name_ar': 'التاريخ'},
            'geographie': {'name': 'Géographie', 'name_ar': 'الجغرافيا'},
            'anglais': {'name': 'Anglais', 'name_ar': 'الإنجليزية'},
            'islamique': {'name': 'Éducation Islamique', 'name_ar': 'التربية الإسلامية'},
            'eps': {'name': 'Éducation Physique', 'name_ar': 'التربية البدنية'},
            'informatique': {'name': 'Informatique', 'name_ar': 'المعلوماتية'}
        }
    
    def validate_levels(self, levels: List[Dict]) -> Dict[str, Any]:
        """Validate education levels against official standards"""
        issues = []
        missing_levels = []
        
        # Check for missing levels
        found_level_ids = {level['id'] for level in levels}
        for level_id, level_info in self.official_levels.items():
            if level_id not in found_level_ids:
                missing_levels.append({
                    'id': level_id,
                    'name': level_info['name'],
                    'name_ar': level_info['name_ar'],
                    'order': level_info['order'],
                    'category': level_info['category']
                })
        
        # Validate existing levels
        for level in levels:
            level_id = level.get('id')
            if level_id in self.official_levels:
                official = self.official_levels[level_id]
                
                # Check name accuracy
                if level.get('name') != official['name']:
                    issues.append(f"Level {level_id}: Name mismatch - found '{level.get('name')}', expected '{official['name']}'")
                
                # Check Arabic name accuracy
                if level.get('name_ar') != official['name_ar']:
                    issues.append(f"Level {level_id}: Arabic name mismatch - found '{level.get('name_ar')}', expected '{official['name_ar']}'")
                
                # Check order
                if level.get('order') != official['order']:
                    issues.append(f"Level {level_id}: Order mismatch - found {level.get('order')}, expected {official['order']}")
        
        return {
            'valid': len(issues) == 0 and len(missing_levels) == 0,
            'issues': issues,
            'missing_levels': missing_levels,
            'completeness': (len(levels) / len(self.official_levels)) * 100
        }
    
    def validate_subjects(self, subjects: List[Dict]) -> Dict[str, Any]:
        """Validate subjects against core curriculum requirements"""
        issues = []
        missing_subjects = []
        
        # Check for missing core subjects
        found_subject_ids = {subject['id'] for subject in subjects}
        for subject_id, subject_info in self.core_subjects.items():
            if subject_id not in found_subject_ids:
                missing_subjects.append({
                    'id': subject_id,
                    'name': subject_info['name'],
                    'name_ar': subject_info['name_ar']
                })
        
        # Validate existing subjects
        for subject in subjects:
            subject_id = subject.get('id')
            
            # Check required fields
            required_fields = ['id', 'name', 'name_ar', 'level_id']
            for field in required_fields:
                if field not in subject or not subject[field]:
                    issues.append(f"Subject {subject_id}: Missing required field '{field}'")
            
            # Check level_id validity
            if subject.get('level_id') and subject['level_id'] not in self.official_levels:
                issues.append(f"Subject {subject_id}: Invalid level_id '{subject['level_id']}'")
        
        return {
            'valid': len(issues) == 0 and len(missing_subjects) == 0,
            'issues': issues,
            'missing_subjects': missing_subjects,
            'completeness': (len(subjects) / len(self.core_subjects)) * 100
        }
    
    def validate_content(self, content: List[Dict]) -> Dict[str, Any]:
        """Validate educational content"""
        issues = []
        
        for item in content:
            item_id = item.get('id')
            
            # Check required fields
            required_fields = ['id', 'title', 'level_id', 'content_type']
            for field in required_fields:
                if field not in item or not item[field]:
                    issues.append(f"Content {item_id}: Missing required field '{field}'")
            
            # Check level_id validity
            if item.get('level_id') and item['level_id'] not in self.official_levels:
                issues.append(f"Content {item_id}: Invalid level_id '{item['level_id']}'")
            
            # Check content_type validity
            valid_types = ['cours', 'exercice', 'examen', 'controle', 'correction']
            if item.get('content_type') and item['content_type'] not in valid_types:
                issues.append(f"Content {item_id}: Invalid content_type '{item['content_type']}'")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'total_items': len(content)
        }
    
    def validate_dataset(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive dataset validation"""
        results = {
            'levels': self.validate_levels(data.get('levels', [])),
            'subjects': self.validate_subjects(data.get('subjects', [])),
            'content': self.validate_content(data.get('content', [])),
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate overall quality score
        level_score = results['levels']['completeness'] / 100
        subject_score = results['subjects']['completeness'] / 100
        content_valid = 1.0 if results['content']['valid'] else 0.5
        
        results['overall_score'] = (level_score + subject_score + content_valid) / 3
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []
        
        if results['levels']['missing_levels']:
            recommendations.append(f"Add {len(results['levels']['missing_levels'])} missing education levels")
        
        if results['subjects']['missing_subjects']:
            recommendations.append(f"Add {len(results['subjects']['missing_subjects'])} missing core subjects")
        
        if results['levels']['issues']:
            recommendations.append(f"Fix {len(results['levels']['issues'])} level data issues")
        
        if results['subjects']['issues']:
            recommendations.append(f"Fix {len(results['subjects']['issues'])} subject data issues")
        
        if results['content']['issues']:
            recommendations.append(f"Fix {len(results['content']['issues'])} content data issues")
        
        if results['overall_score'] < 0.8:
            recommendations.append("Overall data quality needs significant improvement")
        elif results['overall_score'] < 0.95:
            recommendations.append("Data quality is good but needs minor improvements")
        else:
            recommendations.append("Data quality is excellent - ready for production")
        
        return recommendations


def validate_existing_data():
    """Validate current data files"""
    validator = MoroccanEducationValidator()
    
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
    print(f"📊 Validating: {latest_file.name}")
    
    # Load and validate data
    with open(latest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = validator.validate_dataset(data)
    
    # Print results
    print("\n" + "="*70)
    print("📊 DATA VALIDATION RESULTS")
    print("="*70)
    
    print(f"\n🎯 Overall Quality Score: {results['overall_score']:.2f}/1.0")
    
    print(f"\n📚 Levels: {results['levels']['completeness']:.1f}% complete")
    if results['levels']['missing_levels']:
        print(f"   Missing: {len(results['levels']['missing_levels'])} levels")
    if results['levels']['issues']:
        print(f"   Issues: {len(results['levels']['issues'])}")
    
    print(f"\n📖 Subjects: {results['subjects']['completeness']:.1f}% complete")
    if results['subjects']['missing_subjects']:
        print(f"   Missing: {len(results['subjects']['missing_subjects'])} subjects")
    if results['subjects']['issues']:
        print(f"   Issues: {len(results['subjects']['issues'])}")
    
    print(f"\n📄 Content: {results['content']['total_items']} items")
    if results['content']['issues']:
        print(f"   Issues: {len(results['content']['issues'])}")
    
    print(f"\n💡 Recommendations:")
    for rec in results['recommendations']:
        print(f"   - {rec}")
    
    print("\n" + "="*70)
    
    return results


if __name__ == "__main__":
    validate_existing_data()
