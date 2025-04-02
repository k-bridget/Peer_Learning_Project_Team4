def view_performance_ratings(auth_system):
    """Display performance ratings"""
    print("\n--- Doctor Performance Ratings ---")
    ratings = auth_system.get_performance_ratings()
    
    if not ratings:
        print("No ratings found.")
        return
    
    print("\nPerformance Records:")
    for rating in ratings:
        print(f"ID: {rating[0]} | Doctor: {rating[1]} | Rating: {rating[2]}/5 | Date: {rating[3]}")
