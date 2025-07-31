#!/usr/bin/env python3
"""
Script to remove duplicate showNotification functions from HTML templates
"""

import os
import re

def remove_duplicate_shownotification(file_path):
    """Remove duplicate showNotification function from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match the showNotification function
        pattern = r'function showNotification\(message, type = \'info\'\) \{[^}]*\{[^}]*\}[^}]*\{[^}]*\}[^}]*\{[^}]*\}[^}]*\}'
        
        # More comprehensive pattern
        pattern = r'function showNotification\([^)]*\) \{(?:[^{}]*\{[^{}]*\})*[^{}]*\}'
        
        # Even more comprehensive pattern to handle nested braces
        start_pattern = r'function showNotification\(message, type = \'info\'\) \{'
        
        if 'function showNotification' in content:
            # Find the start of the function
            start_match = re.search(start_pattern, content)
            if start_match:
                start_pos = start_match.start()
                
                # Find the matching closing brace
                brace_count = 0
                pos = start_match.end() - 1  # Start from the opening brace
                
                while pos < len(content):
                    if content[pos] == '{':
                        brace_count += 1
                    elif content[pos] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = pos + 1
                            break
                    pos += 1
                else:
                    print(f"Could not find matching brace in {file_path}")
                    return False
                
                # Remove the function and any trailing newlines
                before = content[:start_pos]
                after = content[end_pos:]
                
                # Clean up extra newlines
                while before.endswith('\n\n\n'):
                    before = before[:-1]
                while after.startswith('\n\n\n'):
                    after = after[1:]
                
                new_content = before + '\n\n' + after
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✓ Removed duplicate showNotification from {os.path.basename(file_path)}")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    templates_dir = 'templates'
    files_to_fix = [
        'news.html',
        'lost_found.html', 
        'polls.html',
        'complaints.html',
        'skills.html',
        'login.html'
    ]
    
    print("🔧 Fixing duplicate showNotification functions...")
    print("=" * 50)
    
    fixed_count = 0
    for filename in files_to_fix:
        file_path = os.path.join(templates_dir, filename)
        if os.path.exists(file_path):
            if remove_duplicate_shownotification(file_path):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("=" * 50)
    print(f"🎉 Fixed {fixed_count} files")
    print("All templates now use the centralized showNotification function from main.js")

if __name__ == "__main__":
    main()