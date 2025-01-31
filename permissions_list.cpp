
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 
#include <iostream>
#include <array>
#include <string>

namespace py = pybind11;

std::array<std::string, 2> permissions() {
    return {"leitura", "escrita"};
}

PYBIND11_MODULE(permissions_list, m) {
    m.doc() = "Retorna a lista de permissões";
    m.def("permissions", &permissions, "Retorna a lista de permissões");
}