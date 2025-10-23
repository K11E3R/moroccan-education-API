#!/usr/bin/env python3
"""
Comprehensive Moroccan Education Data Collection Pipeline
Runs complete data collection, validation, correction, and quality monitoring
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add collectors to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'collectors'))

from data_validator import MoroccanEducationValidator
from manual_data_corrector import ManualDataCorrector
from quality_monitor import DataQualityMonitor


class ComprehensiveDataPipeline:
    """Complete data collection and processing pipeline"""
    
    def __init__(self):
        self.validator = MoroccanEducationValidator()
        self.corrector = ManualDataCorrector()
        self.monitor = DataQualityMonitor()
        
        self.pipeline_stats = {
            'start_time': None,
            'end_time': None,
            'steps_completed': [],
            'errors': [],
            'quality_score': 0.0,
            'final_status': 'unknown'
        }
    
    def log_step(self, step_name: str, status: str = "completed"):
        """Log pipeline step completion"""
        self.pipeline_stats['steps_completed'].append({
            'step': step_name,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        print(f"✅ {step_name}: {status}")
    
    def log_error(self, error: str):
        """Log pipeline error"""
        self.pipeline_stats['errors'].append({
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        print(f"❌ Error: {error}")
    
    def find_latest_data_file(self) -> Path:
        """Find the latest data file"""
        # Check multiple directories
        directories = [
            Path("data/raw"),
            Path("data/corrected"),
            Path("data/multi_source")
        ]
        
        latest_file = None
        latest_time = 0
        
        for directory in directories:
            if directory.exists():
                json_files = list(directory.glob("*.json"))
                for file in json_files:
                    if file.stat().st_mtime > latest_time:
                        latest_time = file.stat().st_mtime
                        latest_file = file
        
        return latest_file
    
    def validate_data(self, data_file: Path) -> dict:
        """Validate data file"""
        print(f"📊 Validating data from: {data_file.name}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = self.validator.validate_dataset(data)
        
        print(f"🎯 Validation Score: {results['overall_score']:.2f}/1.0")
        print(f"📚 Levels: {results['levels']['completeness']:.1f}% complete")
        print(f"📖 Subjects: {results['subjects']['completeness']:.1f}% complete")
        
        if results['overall_score'] >= 0.9:
            print("✅ Data quality is EXCELLENT!")
        elif results['overall_score'] >= 0.8:
            print("⚠️ Data quality is GOOD but needs minor improvements")
        else:
            print("❌ Data quality needs significant improvement")
        
        return results
    
    def correct_data(self, data_file: Path) -> Path:
        """Correct data issues"""
        print(f"🔧 Correcting data from: {data_file.name}")
        
        corrected_data = self.corrector.correct_data(data_file)
        
        # Save corrected data
        corrected_dir = Path("data/corrected")
        corrected_file = self.corrector.save_corrected_data(corrected_data, corrected_dir)
        
        return corrected_file
    
    def monitor_quality(self, data_file: Path) -> dict:
        """Monitor data quality"""
        print(f"📊 Monitoring quality of: {data_file.name}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        report = self.monitor.generate_quality_report(data)
        self.monitor.print_quality_report(report)
        
        # Save quality report
        reports_dir = Path("data/quality_reports")
        self.monitor.save_quality_report(report, reports_dir)
        
        return report
    
    def update_api_data(self, data_file: Path) -> bool:
        """Update API with latest data"""
        try:
            api_data_file = Path("api/data.json")
            
            # Copy data to API
            with open(data_file, 'r', encoding='utf-8') as src:
                data = json.load(src)
            
            with open(api_data_file, 'w', encoding='utf-8') as dst:
                json.dump(data, dst, ensure_ascii=False, indent=2)
            
            print(f"✅ Updated API data from: {data_file.name}")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to update API data: {e}")
            return False
    
    def generate_pipeline_report(self) -> dict:
        """Generate comprehensive pipeline report"""
        duration = None
        if self.pipeline_stats['start_time'] and self.pipeline_stats['end_time']:
            start = datetime.fromisoformat(self.pipeline_stats['start_time'])
            end = datetime.fromisoformat(self.pipeline_stats['end_time'])
            duration = (end - start).total_seconds()
        
        report = {
            'pipeline_version': '1.0',
            'execution_time': datetime.now().isoformat(),
            'duration_seconds': duration,
            'steps_completed': self.pipeline_stats['steps_completed'],
            'errors': self.pipeline_stats['errors'],
            'quality_score': self.pipeline_stats['quality_score'],
            'final_status': self.pipeline_stats['final_status'],
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def generate_recommendations(self) -> list:
        """Generate pipeline recommendations"""
        recommendations = []
        
        if self.pipeline_stats['quality_score'] >= 0.95:
            recommendations.append("Data quality is excellent - ready for production")
            recommendations.append("Consider implementing automated data updates")
        elif self.pipeline_stats['quality_score'] >= 0.85:
            recommendations.append("Data quality is good - minor improvements needed")
            recommendations.append("Review and fix remaining validation issues")
        else:
            recommendations.append("Data quality needs significant improvement")
            recommendations.append("Implement additional data sources")
            recommendations.append("Review data collection methodology")
        
        if self.pipeline_stats['errors']:
            recommendations.append(f"Address {len(self.pipeline_stats['errors'])} pipeline errors")
        
        return recommendations
    
    def save_pipeline_report(self, report: dict):
        """Save pipeline report"""
        reports_dir = Path("data/pipeline_reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = reports_dir / f"pipeline_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Pipeline report saved to: {filename}")
        return filename
    
    def run_complete_pipeline(self):
        """Run the complete data processing pipeline"""
        print("="*70)
        print("🚀 COMPREHENSIVE MOROCCAN EDUCATION DATA PIPELINE")
        print("="*70)
        
        self.pipeline_stats['start_time'] = datetime.now().isoformat()
        
        try:
            # Step 1: Find latest data file
            print("\n📁 Step 1: Finding latest data file...")
            data_file = self.find_latest_data_file()
            
            if not data_file:
                raise Exception("No data file found")
            
            print(f"✅ Found data file: {data_file.name}")
            self.log_step("Find data file")
            
            # Step 2: Validate data
            print("\n📊 Step 2: Validating data...")
            validation_results = self.validate_data(data_file)
            self.pipeline_stats['quality_score'] = validation_results['overall_score']
            self.log_step("Validate data")
            
            # Step 3: Correct data if needed
            if validation_results['overall_score'] < 0.9:
                print("\n🔧 Step 3: Correcting data...")
                corrected_file = self.correct_data(data_file)
                data_file = corrected_file
                self.log_step("Correct data")
                
                # Re-validate corrected data
                print("\n📊 Step 3.1: Re-validating corrected data...")
                validation_results = self.validate_data(data_file)
                self.pipeline_stats['quality_score'] = validation_results['overall_score']
                self.log_step("Re-validate corrected data")
            else:
                print("\n✅ Step 3: Data quality is sufficient, skipping correction")
                self.log_step("Skip correction", "data quality sufficient")
            
            # Step 4: Monitor quality
            print("\n📊 Step 4: Monitoring data quality...")
            quality_report = self.monitor_quality(data_file)
            self.log_step("Monitor quality")
            
            # Step 5: Update API
            print("\n🔄 Step 5: Updating API data...")
            api_updated = self.update_api_data(data_file)
            if api_updated:
                self.log_step("Update API data")
            else:
                self.log_error("Failed to update API data")
            
            # Step 6: Generate final report
            print("\n📊 Step 6: Generating pipeline report...")
            pipeline_report = self.generate_pipeline_report()
            self.save_pipeline_report(pipeline_report)
            self.log_step("Generate pipeline report")
            
            # Determine final status
            if self.pipeline_stats['quality_score'] >= 0.9:
                self.pipeline_stats['final_status'] = 'excellent'
            elif self.pipeline_stats['quality_score'] >= 0.8:
                self.pipeline_stats['final_status'] = 'good'
            else:
                self.pipeline_stats['final_status'] = 'needs_improvement'
            
            self.pipeline_stats['end_time'] = datetime.now().isoformat()
            
            # Final summary
            print("\n" + "="*70)
            print("📊 PIPELINE EXECUTION COMPLETE")
            print("="*70)
            print(f"🎯 Final Quality Score: {self.pipeline_stats['quality_score']:.2f}/1.0")
            print(f"📊 Final Status: {self.pipeline_stats['final_status'].upper()}")
            print(f"✅ Steps Completed: {len(self.pipeline_stats['steps_completed'])}")
            print(f"❌ Errors: {len(self.pipeline_stats['errors'])}")
            
            if self.pipeline_stats['final_status'] == 'excellent':
                print("\n🎉 SUCCESS: Data is ready for production!")
                print("   - API has been updated with corrected data")
                print("   - Quality monitoring is active")
                print("   - All validation checks passed")
            elif self.pipeline_stats['final_status'] == 'good':
                print("\n⚠️ PARTIAL SUCCESS: Data is good but needs minor improvements")
                print("   - API has been updated")
                print("   - Review recommendations for improvements")
            else:
                print("\n❌ NEEDS IMPROVEMENT: Data quality requires attention")
                print("   - Review pipeline errors")
                print("   - Implement recommended improvements")
            
            print("\n💡 Recommendations:")
            for rec in pipeline_report['recommendations']:
                print(f"   - {rec}")
            
            print("\n" + "="*70)
            
            return pipeline_report
            
        except Exception as e:
            self.log_error(f"Pipeline execution failed: {e}")
            self.pipeline_stats['end_time'] = datetime.now().isoformat()
            self.pipeline_stats['final_status'] = 'failed'
            
            print(f"\n❌ PIPELINE FAILED: {e}")
            return self.generate_pipeline_report()


def main():
    """Main pipeline execution"""
    pipeline = ComprehensiveDataPipeline()
    report = pipeline.run_complete_pipeline()
    
    # Exit with appropriate code
    if pipeline.pipeline_stats['final_status'] == 'excellent':
        exit(0)
    elif pipeline.pipeline_stats['final_status'] == 'good':
        exit(1)
    else:
        exit(2)


if __name__ == "__main__":
    main()
