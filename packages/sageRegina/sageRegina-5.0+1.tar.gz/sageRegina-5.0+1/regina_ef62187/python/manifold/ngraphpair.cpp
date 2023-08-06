
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
#include "manifold/ngraphpair.h"
#include "manifold/nsfs.h"
#include "../helpers.h"

using namespace boost::python;
using regina::NGraphPair;
using regina::NMatrix2;
using regina::NSFSpace;

namespace {
    NGraphPair* createNGraphPair_longs(const NSFSpace& s1, const NSFSpace& s2,
            long a, long b, long c, long d) {
        return new NGraphPair(new NSFSpace(s1), new NSFSpace(s2), a, b, c, d);
    }

    NGraphPair* createNGraphPair_matrix(const NSFSpace& s1, const NSFSpace& s2,
            const NMatrix2& m) {
        return new NGraphPair(new NSFSpace(s1), new NSFSpace(s2), m);
    }
}

void addNGraphPair() {
    class_<NGraphPair, bases<regina::NManifold>,
            std::auto_ptr<NGraphPair>, boost::noncopyable>
            ("NGraphPair", no_init)
        .def("__init__", make_constructor(createNGraphPair_longs))
        .def("__init__", make_constructor(createNGraphPair_matrix))
        .def("sfs", &NGraphPair::sfs,
            return_internal_reference<>())
        .def("matchingReln", &NGraphPair::matchingReln,
            return_internal_reference<>())
        .def(self < self)
        .def(regina::python::add_eq_operators())
    ;

    implicitly_convertible<std::auto_ptr<NGraphPair>,
        std::auto_ptr<regina::NManifold> >();
}

