#!/usr/bin/env python3
"""
Test script for issue notification feature
Tests the complete workflow: CSV import, email notification, and notification status tracking
"""

import sys
import os
sys.path.append('.')

from app import create_app
from app.models.issue import Issue
from app.models.category import Category
from app.utils.csv_manager import CsvManager
from app.utils.email_notifier import MockEmailNotifier
from app.utils.csv_importer import CsvImporter

def create_test_csv_content():
    """Create test CSV content with issues for different specific functions"""
    return """create_time,Carline,Power,Specific Function,Function Domain,General Domain,Issue Type,Description,Description En,Brief_Issue,Brief_Issue_En
2024-01-15,A-Class,Electric,Air Conditioning Control,Climate Control,Comfort,Feature Request,Enhance air conditioning control function,Enhance air conditioning control function,Enhance air conditioning control function,Enhance air conditioning control function
2024-01-16,C-Class,Hybrid,Air Conditioning Control,Climate Control,Comfort,Bug,Air conditioning not working properly,Air conditioning not working properly,Air conditioning not working properly,Air conditioning not working properly
2024-01-17,E-Class,Gasoline,Remote Control Function,Infotainment,Entertainment,Feature Request,Add remote control capability,Add remote control capability,Add remote control capability,Add remote control capability
2024-01-18,S-Class,Electric,Remote Control Function,Infotainment,Entertainment,Bug,Remote control connection issues,Remote control connection issues,Remote control connection issues,Remote control connection issues
2024-01-19,A-Class,Hybrid,Camera System,Safety,Driver Assistance,Feature Request,Improve rear camera quality,Improve rear camera quality,Improve rear camera quality,Improve rear camera quality"""

def create_test_categories():
    """Create test categories with email configurations"""
    categories = [
        Category(
            specific_function="Air Conditioning Control",
            function_domain="Climate Control",
            general_domain="Comfort"
        ),
        Category(
            specific_function="Remote Control Function",
            function_domain="Infotainment",
            general_domain="Entertainment"
        ),
        Category(
            specific_function="Camera System",
            function_domain="Safety",
            general_domain="Driver Assistance"
        )
    ]
    
    # Set email lists for testing
    categories[0].set_email_list(["test1@example.com", "test2@example.com"])
    categories[1].set_email_list(["test3@example.com"])
    categories[2].set_email_list([])  # No emails configured
    
    return categories

def test_notification_feature():
    """Test the complete notification feature"""
    print("=== Testing Issue Notification Feature ===\n")
    
    app = create_app()
    with app.app_context():
        # Initialize managers
        issue_manager = CsvManager('data/test_issues.csv', Issue)
        category_manager = CsvManager('data/test_categories.csv', Category)
        
        # Clear existing data
        issue_manager.write_all([])
        category_manager.write_all([])
        
        # Create test categories
        test_categories = create_test_categories()
        for category in test_categories:
            category_manager.add_item(category)
        
        print(f"✓ Created {len(test_categories)} test categories with email configurations")
        
        # Create mock email notifier
        email_notifier = MockEmailNotifier()
        email_notifier.clear_sent_emails()
        
        print("✓ Initialized mock email notifier")
        
        # Test CSV import with notification
        csv_content = create_test_csv_content()
        print(f"✓ Created test CSV content with 5 issues")
        
        # Import CSV with notification
        import_result = CsvImporter.import_from_directvoice_format(
            csv_content, issue_manager, category_manager, email_notifier
        )
        
        print(f"\n=== Import Results ===")
        print(f"Imported: {import_result['imported_count']} issues")
        print(f"Skipped: {import_result['skipped_count']} issues")
        print(f"Batch ID: {import_result['batch_id']}")
        
        if import_result['errors']:
            print(f"Errors: {len(import_result['errors'])}")
            for error in import_result['errors']:
                print(f"  - {error}")
        
        # Check notification results
        print(f"\n=== Notification Results ===")
        notification_results = import_result.get('notification_results', [])
        for result in notification_results:
            print(f"Specific Function: {result['specific_function']}")
            print(f"  Status: {result['status']}")
            if result['status'] == 'success':
                print(f"  Recipients: {result['recipients']}")
                print(f"  Issue Count: {result['issue_count']}")
            elif result['status'] == 'skipped':
                print(f"  Reason: {result['reason']}")
            else:
                print(f"  Reason: {result['reason']}")
            print()
        
        # Verify email notifications
        sent_emails = email_notifier.get_sent_emails()
        print(f"=== Email Verification ===")
        print(f"Total emails sent: {len(sent_emails)}")
        
        for i, email_data in enumerate(sent_emails, 1):
            print(f"\nEmail {i}:")
            print(f"  To: {email_data['to_emails']}")
            print(f"  Specific Function: {email_data['specific_function']}")
            print(f"  Issues: {len(email_data['issues'])}")
            print(f"  Batch ID: {email_data['batch_id']}")
        
        # Verify issue notification status
        print(f"\n=== Issue Notification Status ===")
        all_issues = issue_manager.read_all()
        notified_count = sum(1 for issue in all_issues if issue.notified == 1)
        not_notified_count = sum(1 for issue in all_issues if issue.notified == 0)
        
        print(f"Total issues: {len(all_issues)}")
        print(f"Notified: {notified_count}")
        print(f"Not notified: {not_notified_count}")
        
        # Show details for each issue
        for issue in all_issues:
            print(f"  Issue #{issue.global_id}: {issue.specific_function} - Notified: {issue.notified}")
        
        # Test specific function grouping
        print(f"\n=== Specific Function Grouping ===")
        issues_by_function = {}
        for issue in all_issues:
            func = issue.specific_function
            if func not in issues_by_function:
                issues_by_function[func] = []
            issues_by_function[func].append(issue)
        
        for func, issues in issues_by_function.items():
            print(f"{func}: {len(issues)} issues")
            notified_in_group = sum(1 for issue in issues if issue.notified == 1)
            print(f"  - Notified: {notified_in_group}/{len(issues)}")
        
        # Cleanup
        issue_manager.write_all([])
        category_manager.write_all([])
        print(f"\n✓ Cleaned up test data")
        
        print(f"\n=== Test Summary ===")
        print(f"✓ CSV import with notification: {'PASS' if import_result['imported_count'] == 5 else 'FAIL'}")
        print(f"✓ Email notifications sent: {'PASS' if len(sent_emails) == 2 else 'FAIL'} (expected 2 for functions with emails)")
        print(f"✓ Notification status tracking: {'PASS' if notified_count > 0 else 'FAIL'}")
        
        return {
            'import_success': import_result['imported_count'] == 5,
            'notification_success': len(sent_emails) == 2,
            'status_tracking_success': notified_count > 0
        }

if __name__ == "__main__":
    try:
        results = test_notification_feature()
        print(f"\n🎉 All tests completed!")
        print(f"Overall result: {'PASS' if all(results.values()) else 'FAIL'}")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc() 