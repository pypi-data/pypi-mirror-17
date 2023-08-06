#include <turbodbc/cursor.h>

#include <boost/python/class.hpp>

namespace turbodbc { namespace bindings {

void for_cursor()
{
	boost::python::class_<turbodbc::cursor>("Cursor", boost::python::no_init)
			.def("prepare", &turbodbc::cursor::prepare)
			.def("execute", &turbodbc::cursor::execute)
			.def("add_parameter_set", &turbodbc::cursor::add_parameter_set)
			.def("get_row_count", &turbodbc::cursor::get_row_count)
			.def("get_result_set", &turbodbc::cursor::get_result_set)
		;
}

} }
