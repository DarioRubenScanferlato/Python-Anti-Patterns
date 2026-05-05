import timeit

def benchmark_conditional_loop():
    data = range(100000)
    
    # Traditional loop
    def traditional():
        result = []
        for x in data:
            if x % 2 == 0:
                result.append(x ** 2)
        return result
    
    # List comprehension
    def list_comp():
        return [x ** 2 for x in data if x % 2 == 0]
    
    # Generator expression (consumed)
    def gen_expr():
        return list(x ** 2 for x in data if x % 2 == 0)

    def map_filter():
        return list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, data)))
    
    # Benchmark results (seconds for 100 iterations)
    traditional_time = timeit.timeit(traditional, number=100)
    list_comp_time = timeit.timeit(list_comp, number=100)
    gen_expr_time = timeit.timeit(gen_expr, number=100)
    map_filter_time = timeit.timeit(map_filter, number=100)
    
    print(f"Traditional loop: {traditional_time:.4f}s")
    print(f"List comprehension: {list_comp_time:.4f}s")  
    print(f"Generator expression: {gen_expr_time:.4f}s")
    print(f"Using map and filter: {map_filter_time:.4f}s")


def benchmark_sum():
    data = range(100000)
    
    # Traditional loop
    def traditional():
        result = 0
        for x in data:
            result += x ** 2
        return result
    
    # List comprehension
    def list_comp():
        return sum([x ** 2 for x in data])
    
    # Generator expression (consumed)
    def gen_expr():
        return sum(x ** 2 for x in data)

    def using_map():
        return sum(map(lambda x: x ** 2, data))
    
    # Benchmark results (seconds for 100 iterations)
    traditional_time = timeit.timeit(traditional, number=100)
    list_comp_time = timeit.timeit(list_comp, number=100)
    gen_expr_time = timeit.timeit(gen_expr, number=100)
    map_time = timeit.timeit(using_map, number=100)
    
    print(f"Traditional loop: {traditional_time:.4f}s")
    print(f"List comprehension: {list_comp_time:.4f}s") 
    print(f"Generator expression: {gen_expr_time:.4f}s")
    print(f"Using map: {map_time:.4f}s")


if __name__ == "__main__":
    print("Benchmarking conditional loop vs list comprehension vs generator expression:")
    benchmark_conditional_loop()
    print("Benchmarking sum with traditional loop vs list comprehension vs generator expression:")
    benchmark_sum()