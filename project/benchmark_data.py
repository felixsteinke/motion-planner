class BenchmarkData:
    def __init__(self, name: str, runs: int = 25):
        self.__name = name
        self.__runs = runs
        self.__vertices = 0
        self.__max_vertices = 0
        self.__min_vertices = 99999999
        self.__edges = 0
        self.__max_edges = 0
        self.__min_edges = 99999999
        self.__time = 0
        self.__max_time = 0
        self.__min_time = 99999999
        self.__solutions = runs
        self.__solution_nodes = 0
        self.__max_solution_nodes = 0
        self.__min_solution_nodes = 99999999
        self.__solution_length = 0
        self.__max_solution_length = 0
        self.__min_solution_length = 99999999

    def add_run_data(self, vertex_array: [], edge_array: [], calc_time: int, solution_array: [], solution_length: int):
        run_vertices = len(vertex_array)
        self.__vertices += run_vertices
        if run_vertices > self.__max_vertices:
            self.__max_vertices = run_vertices
        if run_vertices < self.__min_vertices:
            self.__min_vertices = run_vertices

        run_edges = len(edge_array)
        self.__edges += run_edges
        if run_edges > self.__max_edges:
            self.__max_edges = run_edges
        if run_edges < self.__min_edges:
            self.__min_edges = run_edges

        self.__time += calc_time
        if calc_time > self.__max_time:
            self.__max_time = calc_time
        if calc_time < self.__min_time:
            self.__min_time = calc_time

        if solution_array:
            run_solution_nodes = len(solution_array)
            self.__solution_nodes += run_solution_nodes
            if run_solution_nodes > self.__max_solution_nodes:
                self.__max_solution_nodes = run_solution_nodes
            if len(solution_array) < self.__min_solution_nodes:
                self.__min_solution_nodes = run_solution_nodes

            self.__solution_length += solution_length
            if solution_length > self.__max_solution_length:
                self.__max_solution_length = solution_length
            if solution_length < self.__min_solution_length:
                self.__min_solution_length = solution_length
        else:
            self.__solutions -= 1

    def __calc_average(self) -> None:
        self.__vertices /= self.__runs
        self.__edges /= self.__runs
        self.__time /= self.__runs
        if self.__solutions:
            self.__solution_nodes /= self.__solutions
            self.__solution_length /= self.__solutions

    def get_result(self) -> str:
        self.__calc_average()
        return '[BENCHMARK] {}: runs={}, solutions={}\n' \
               'Vertices: avg={}, min={}, max={}\n' \
               'Edges: avg={}, min={}, max={}\n' \
               'Times (sec): avg={}, min={}, max={}\n' \
               'Solution Nodes: avg={}, min={}, max={}\n' \
               'Solution Length: avg={}, min={}, max={}' \
            .format(self.__name, self.__runs, self.__solutions,
                    self.__vertices, self.__min_vertices, self.__max_vertices,
                    self.__edges, self.__min_edges, self.__max_edges,
                    round(self.__time, 5), round(self.__min_time, 5), round(self.__max_time, 5),
                    self.__solution_nodes, self.__min_solution_nodes, self.__max_solution_nodes,
                    self.__solution_length, self.__min_solution_length, self.__max_solution_length)
