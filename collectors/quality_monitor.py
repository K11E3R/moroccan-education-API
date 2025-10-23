"""
Comprehensive Data Quality Monitoring System
Monitors and reports on data quality metrics in real-time
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collectors.data_validator import MoroccanEducationValidator


class DataQualityMonitor:
    """Monitors data quality and generates comprehensive reports"""
    
    def __init__(self):
        self.validator = MoroccanEducationValidator()
        self.quality_thresholds = {
            'excellent': 0.95,
            'good': 0.85,
            'acceptable': 0.75,
            'poor': 0.60
        }
    
    def calculate_completeness_score(self, data: Dict[str, Any]) -> float:
        """Calculate data completeness score"""
        levels_score = len(data.get('levels', [])) / len(self.validator.official_levels)
        subjects_score = len(data.get('subjects', [])) / (len(self.validator.core_subjects) * 12)  # 12 levels
        content_score = min(len(data.get('content', [])) / 1000, 1.0)  # Expect at least 1000 content items
        
        return (levels_score + subjects_score + content_score) / 3
    
    def calculate_accuracy_score(self, data: Dict[str, Any]) -> float:
        """Calculate data accuracy score"""
        accuracy_issues = 0
        total_items = 0
        
        # Check level accuracy
        for level in data.get('levels', []):
            total_items += 1
            level_id = level.get('id')
            if level_id in self.validator.official_levels:
                official = self.validator.official_levels[level_id]
                if level.get('name') != official['name']:
                    accuracy_issues += 1
                if level.get('name_ar') != official['name_ar']:
                    accuracy_issues += 1
            else:
                accuracy_issues += 1
        
        # Check subject accuracy
        for subject in data.get('subjects', []):
            total_items += 1
            subject_id = subject.get('id', '').split('-')[0]
            if subject_id in self.validator.core_subjects:
                official = self.validator.core_subjects[subject_id]
                if subject.get('name') != official['name']:
                    accuracy_issues += 1
                if subject.get('name_ar') != official['name_ar']:
                    accuracy_issues += 1
            else:
                accuracy_issues += 1
        
        if total_items == 0:
            return 0.0
        
        return max(0.0, 1.0 - (accuracy_issues / total_items))
    
    def calculate_consistency_score(self, data: Dict[str, Any]) -> float:
        """Calculate data consistency score"""
        consistency_issues = 0
        total_checks = 0
        
        # Check level consistency
        level_ids = {level['id'] for level in data.get('levels', [])}
        for subject in data.get('subjects', []):
            total_checks += 1
            if subject.get('level_id') not in level_ids:
                consistency_issues += 1
        
        # Check content consistency
        subject_ids = {subject['id'] for subject in data.get('subjects', [])}
        for content in data.get('content', []):
            total_checks += 1
            if content.get('subject_id') and content['subject_id'] not in subject_ids:
                consistency_issues += 1
        
        if total_checks == 0:
            return 1.0
        
        return max(0.0, 1.0 - (consistency_issues / total_checks))
    
    def calculate_timeliness_score(self, data: Dict[str, Any]) -> float:
        """Calculate data timeliness score"""
        collection_date = data.get('collection_date')
        if not collection_date:
            return 0.0
        
        try:
            collection_time = datetime.fromisoformat(collection_date.replace('Z', '+00:00'))
            days_old = (datetime.now() - collection_time).days
            
            # Data is fresh if less than 7 days old
            if days_old <= 7:
                return 1.0
            elif days_old <= 30:
                return 0.8
            elif days_old <= 90:
                return 0.6
            else:
                return 0.3
        except:
            return 0.0
    
    def calculate_overall_quality_score(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive quality score"""
        completeness = self.calculate_completeness_score(data)
        accuracy = self.calculate_accuracy_score(data)
        consistency = self.calculate_consistency_score(data)
        timeliness = self.calculate_timeliness_score(data)
        
        overall_score = (completeness + accuracy + consistency + timeliness) / 4
        
        # Determine quality level
        if overall_score >= self.quality_thresholds['excellent']:
            quality_level = 'excellent'
        elif overall_score >= self.quality_thresholds['good']:
            quality_level = 'good'
        elif overall_score >= self.quality_thresholds['acceptable']:
            quality_level = 'acceptable'
        else:
            quality_level = 'poor'
        
        return {
            'overall_score': overall_score,
            'quality_level': quality_level,
            'breakdown': {
                'completeness': completeness,
                'accuracy': accuracy,
                'consistency': consistency,
                'timeliness': timeliness
            },
            'thresholds': self.quality_thresholds
        }
    
    def generate_quality_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive quality report"""
        quality_scores = self.calculate_overall_quality_score(data)
        validation_results = self.validator.validate_dataset(data)
        
        # Calculate statistics
        stats = {
            'total_levels': len(data.get('levels', [])),
            'total_subjects': len(data.get('subjects', [])),
            'total_content': len(data.get('content', [])),
            'expected_levels': len(self.validator.official_levels),
            'expected_subjects': len(self.validator.core_subjects) * 12,
            'collection_date': data.get('collection_date', 'Unknown'),
            'last_validation': datetime.now().isoformat()
        }
        
        # Generate recommendations
        recommendations = self.generate_recommendations(quality_scores, validation_results, stats)
        
        # Generate alerts
        alerts = self.generate_alerts(quality_scores, validation_results)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'quality_scores': quality_scores,
            'validation_results': validation_results,
            'statistics': stats,
            'recommendations': recommendations,
            'alerts': alerts,
            'data_source': data.get('base_url', 'Unknown'),
            'report_version': '1.0'
        }
        
        return report
    
    def generate_recommendations(self, quality_scores: Dict[str, Any], validation_results: Dict[str, Any], stats: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Completeness recommendations
        if quality_scores['breakdown']['completeness'] < 0.9:
            missing_levels = stats['expected_levels'] - stats['total_levels']
            if missing_levels > 0:
                recommendations.append(f"Add {missing_levels} missing education levels")
            
            missing_subjects = stats['expected_subjects'] - stats['total_subjects']
            if missing_subjects > 0:
                recommendations.append(f"Add {missing_subjects} missing subject entries")
        
        # Accuracy recommendations
        if quality_scores['breakdown']['accuracy'] < 0.9:
            recommendations.append("Review and correct data accuracy issues")
        
        # Consistency recommendations
        if quality_scores['breakdown']['consistency'] < 0.9:
            recommendations.append("Fix data consistency issues between levels, subjects, and content")
        
        # Timeliness recommendations
        if quality_scores['breakdown']['timeliness'] < 0.8:
            recommendations.append("Update data collection - content may be outdated")
        
        # Overall recommendations
        if quality_scores['overall_score'] < 0.8:
            recommendations.append("Data quality needs significant improvement before production use")
        elif quality_scores['overall_score'] < 0.95:
            recommendations.append("Data quality is good but needs minor improvements")
        else:
            recommendations.append("Data quality is excellent - ready for production")
        
        return recommendations
    
    def generate_alerts(self, quality_scores: Dict[str, Any], validation_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate quality alerts"""
        alerts = []
        
        # Critical alerts
        if quality_scores['overall_score'] < 0.6:
            alerts.append({
                'level': 'critical',
                'message': 'Data quality is critically low',
                'action': 'Immediate data correction required'
            })
        
        # Warning alerts
        if quality_scores['breakdown']['completeness'] < 0.8:
            alerts.append({
                'level': 'warning',
                'message': 'Data completeness is below acceptable threshold',
                'action': 'Add missing levels and subjects'
            })
        
        if quality_scores['breakdown']['accuracy'] < 0.8:
            alerts.append({
                'level': 'warning',
                'message': 'Data accuracy issues detected',
                'action': 'Review and correct data accuracy'
            })
        
        if quality_scores['breakdown']['timeliness'] < 0.6:
            alerts.append({
                'level': 'warning',
                'message': 'Data may be outdated',
                'action': 'Update data collection'
            })
        
        # Info alerts
        if quality_scores['overall_score'] >= 0.95:
            alerts.append({
                'level': 'info',
                'message': 'Data quality is excellent',
                'action': 'Ready for production use'
            })
        
        return alerts
    
    def save_quality_report(self, report: Dict[str, Any], output_dir: Path):
        """Save quality report to file"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"quality_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Quality report saved to: {filename}")
        return filename
    
    def print_quality_report(self, report: Dict[str, Any]):
        """Print formatted quality report"""
        print("\n" + "="*70)
        print("📊 COMPREHENSIVE DATA QUALITY REPORT")
        print("="*70)
        
        # Overall score
        quality_scores = report['quality_scores']
        print(f"\n🎯 Overall Quality Score: {quality_scores['overall_score']:.2f}/1.0 ({quality_scores['quality_level'].upper()})")
        
        # Breakdown
        breakdown = quality_scores['breakdown']
        print(f"\n📈 Quality Breakdown:")
        print(f"   Completeness: {breakdown['completeness']:.2f}/1.0")
        print(f"   Accuracy: {breakdown['accuracy']:.2f}/1.0")
        print(f"   Consistency: {breakdown['consistency']:.2f}/1.0")
        print(f"   Timeliness: {breakdown['timeliness']:.2f}/1.0")
        
        # Statistics
        stats = report['statistics']
        print(f"\n📊 Data Statistics:")
        print(f"   Levels: {stats['total_levels']}/{stats['expected_levels']} ({stats['total_levels']/stats['expected_levels']*100:.1f}%)")
        print(f"   Subjects: {stats['total_subjects']}/{stats['expected_subjects']} ({stats['total_subjects']/stats['expected_subjects']*100:.1f}%)")
        print(f"   Content: {stats['total_content']} items")
        print(f"   Collection Date: {stats['collection_date']}")
        
        # Alerts
        alerts = report['alerts']
        if alerts:
            print(f"\n🚨 Alerts:")
            for alert in alerts:
                level_emoji = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}.get(alert['level'], '⚪')
                print(f"   {level_emoji} {alert['level'].upper()}: {alert['message']}")
                print(f"      Action: {alert['action']}")
        
        # Recommendations
        recommendations = report['recommendations']
        if recommendations:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        print("\n" + "="*70)


def monitor_data_quality(data_file: Path):
    """Monitor quality of a specific data file"""
    monitor = DataQualityMonitor()
    
    print(f"📊 Monitoring data quality for: {data_file.name}")
    
    # Load data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate quality report
    report = monitor.generate_quality_report(data)
    
    # Print report
    monitor.print_quality_report(report)
    
    # Save report
    reports_dir = Path("data/quality_reports")
    saved_report = monitor.save_quality_report(report, reports_dir)
    
    return report


if __name__ == "__main__":
    # Find latest data file to monitor
    data_dir = Path("data/corrected")
    if not data_dir.exists():
        data_dir = Path("data/raw")
    
    if data_dir.exists():
        json_files = list(data_dir.glob("*.json"))
        if json_files:
            latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
            monitor_data_quality(latest_file)
        else:
            print("❌ No JSON data files found")
    else:
        print("❌ No data directory found")
