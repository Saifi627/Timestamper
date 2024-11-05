from django.shortcuts import render
from .forms import TimestampForm

def time_to_seconds(time_str):
    semicolon_error = ';' in time_str
    time_str = time_str.replace(';', ':')
    
    # Check if there's a missing colon after converting semicolons
    if time_str.count(':') < 1:
        raise ValueError("Missing colon or semicolon in timestamp")
    
    parts = time_str.split(':')
    if len(parts) == 2:  # minutes:seconds format
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds, semicolon_error
    elif len(parts) == 3:  # hours:minutes:seconds format
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds, semicolon_error
    else:
        raise ValueError("Incorrect timestamp format")

def calculate_times(request):
    if request.method == 'POST':
        form = TimestampForm(request.POST)
        if form.is_valid():
            time_stamps = [ts for ts in form.cleaned_data['timestamps'].strip().split('\n') if ts.strip()]
            total_secs = []
            results = []
            errors = []
            
            for i, ts in enumerate(time_stamps):
                try:
                    # Clean up the timestamp string
                    ts_clean = ts.replace('(', '').replace(')', '').replace(';', ':')
                    start, end = ts_clean.split('-')
                    
                    # Convert start and end times
                    start_seconds, semicolon_error_start = time_to_seconds(start.strip())
                    end_seconds, semicolon_error_end = time_to_seconds(end.strip())
                    
                    # Calculate duration
                    duration = end_seconds - start_seconds
                    total_secs.append(duration)
                    
                    # Prepare error message if necessary
                    semicolon_error_message = ""
                    if semicolon_error_start or semicolon_error_end:
                        semicolon_error_message = " (semicolon error corrected)"
                    
                    results.append(f"Time Stamp {i+1}: {duration} seconds ({ts}){semicolon_error_message}")
                except ValueError as e:
                    # Handle missing or incorrect delimiters
                    errors.append(f"Error in Time Stamp {i+1}: '{ts}' - {str(e)}")
                    results.append(f"Error in Time Stamp {i+1}: '{ts}' - {str(e)}")
            
            total_time_secs = sum(total_secs)
            total_time_mins = total_time_secs / 60
            context = {
                'form': form,
                'results': results,
                'total_time_secs': total_time_secs,
                'total_time_mins': round(total_time_mins, 2),
                'errors': errors,
            }
            return render(request, 'app_name/results.html', context)
    else:
        form = TimestampForm()
    return render(request, 'app_name/index.html', {'form': form})
