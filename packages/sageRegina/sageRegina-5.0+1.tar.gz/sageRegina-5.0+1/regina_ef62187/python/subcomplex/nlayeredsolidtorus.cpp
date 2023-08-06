
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  Python Interface                                                      *
 *                                                                        *
 *  Copyright (c) 1999-2016, Ben Burton                                   *
 *  For further details contact Ben Burton (bab@debian.org).              *
 *                                                                        *
 *  This program is free software; you can redistribute it and/or         *
 *  modify it under the terms of the GNU General Public License as        *
 *  published by the Free Software Foundation; either version 2 of the    *
 *  License, or (at your option) any later version.                       *
 *                                                                        *
 *  As an exception, when this program is distributed through (i) the     *
 *  App Store by Apple Inc.; (ii) the Mac App Store by Apple Inc.; or     *
 *  (iii) Google Play by Google Inc., then that store may impose any      *
 *  digital rights management, device limits and/or redistribution        *
 *  restrictions that are required by its terms of service.               *
 *                                                                        *
 *  This program is distributed in the hope that it will be useful, but   *
 *  WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     *
 *  General Public License for more details.                              *
 *                                                                        *
 *  You should have received a copy of the GNU General Public             *
 *  License along with this program; if not, write to the Free            *
 *  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,       *
 *  MA 02110-1301, USA.                                                   *
 *                                                                        *
 **************************************************************************/

#include <boost/python.hpp>
#include "subcomplex/nlayeredsolidtorus.h"
#include "triangulation/ntetrahedron.h"
#include "triangulation/ntriangulation.h"
#include "../helpers.h"

using namespace boost::python;
using regina::NLayeredSolidTorus;

void addNLayeredSolidTorus() {
    class_<NLayeredSolidTorus, bases<regina::NStandardTriangulation>,
            std::auto_ptr<NLayeredSolidTorus>, boost::noncopyable>
            ("NLayeredSolidTorus", no_init)
        .def("clone", &NLayeredSolidTorus::clone,
            return_value_policy<manage_new_object>())
        .def("size", &NLayeredSolidTorus::size)
        .def("getNumberOfTetrahedra", &NLayeredSolidTorus::size)
        .def("base", &NLayeredSolidTorus::base,
            return_value_policy<reference_existing_object>())
        .def("getBase", &NLayeredSolidTorus::base,
            return_value_policy<reference_existing_object>())
        .def("baseEdge", &NLayeredSolidTorus::baseEdge)
        .def("getBaseEdge", &NLayeredSolidTorus::baseEdge)
        .def("baseEdgeGroup", &NLayeredSolidTorus::baseEdgeGroup)
        .def("getBaseEdgeGroup", &NLayeredSolidTorus::baseEdgeGroup)
        .def("baseFace", &NLayeredSolidTorus::baseFace)
        .def("getBaseFace", &NLayeredSolidTorus::baseFace)
        .def("topLevel", &NLayeredSolidTorus::topLevel,
            return_value_policy<reference_existing_object>())
        .def("getTopLevel", &NLayeredSolidTorus::topLevel,
            return_value_policy<reference_existing_object>())
        .def("meridinalCuts", &NLayeredSolidTorus::meridinalCuts)
        .def("getMeridinalCuts", &NLayeredSolidTorus::meridinalCuts)
        .def("topEdge", &NLayeredSolidTorus::topEdge)
        .def("getTopEdge", &NLayeredSolidTorus::topEdge)
        .def("topEdgeGroup", &NLayeredSolidTorus::topEdgeGroup)
        .def("getTopEdgeGroup", &NLayeredSolidTorus::topEdgeGroup)
        .def("topFace", &NLayeredSolidTorus::topFace)
        .def("getTopFace", &NLayeredSolidTorus::topFace)
        .def("flatten", &NLayeredSolidTorus::flatten,
            return_value_policy<manage_new_object>())
        .def("transform", &NLayeredSolidTorus::transform)
        .def("formsLayeredSolidTorusBase",
            &NLayeredSolidTorus::formsLayeredSolidTorusBase,
            return_value_policy<manage_new_object>())
        .def("formsLayeredSolidTorusTop",
            &NLayeredSolidTorus::formsLayeredSolidTorusTop,
            return_value_policy<manage_new_object>())
        .def("isLayeredSolidTorus", &NLayeredSolidTorus::isLayeredSolidTorus,
            return_value_policy<manage_new_object>())
        .def(regina::python::add_eq_operators())
        .staticmethod("formsLayeredSolidTorusBase")
        .staticmethod("formsLayeredSolidTorusTop")
        .staticmethod("isLayeredSolidTorus")
    ;

    implicitly_convertible<std::auto_ptr<NLayeredSolidTorus>,
        std::auto_ptr<regina::NStandardTriangulation> >();
}

