
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
#include "algebra/nabeliangroup.h"
#include "manifold/nmanifold.h"
#include "triangulation/ntriangulation.h"
#include "../helpers.h"
#include "../safeheldtype.h"

using namespace boost::python;
using namespace regina::python;
using regina::NManifold;

namespace {
    void writeName_stdio(const NManifold& m) {
        m.writeName(std::cout);
    }
    void writeTeXName_stdio(const NManifold& m) {
        m.writeTeXName(std::cout);
    }
    void writeStructure_stdio(const NManifold& m) {
        m.writeStructure(std::cout);
    }
}

void addNManifold() {
    class_<NManifold, boost::noncopyable, std::auto_ptr<NManifold> >
            ("NManifold", no_init)
        .def("name", &NManifold::name)
        .def("getName", &NManifold::name)
        .def("TeXName", &NManifold::TeXName)
        .def("getTeXName", &NManifold::TeXName)
        .def("structure", &NManifold::structure)
        .def("getStructure", &NManifold::structure)
        .def("construct", &NManifold::construct,
            return_value_policy<to_held_type<> >())
        .def("homology", &NManifold::homology,
            return_value_policy<manage_new_object>())
        .def("homologyH1", &NManifold::homologyH1,
            return_value_policy<manage_new_object>())
        .def("getHomologyH1", &NManifold::homologyH1,
            return_value_policy<manage_new_object>())
        .def("isHyperbolic", &NManifold::isHyperbolic)
        .def("writeName", writeName_stdio)
        .def("writeTeXName", writeTeXName_stdio)
        .def("writeStructure", writeStructure_stdio)
        .def(self < self)
        .def(regina::python::add_output())
        .def(regina::python::add_eq_operators())
    ;
}

