
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  Computational Engine                                                  *
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

#include <sstream>
#include "maths/nperm2.h"

namespace regina {

const NPerm<2>::Index NPerm<2>::nPerms;
const NPerm<2>::Index NPerm<2>::nPerms_1;

const NPerm<2> NPerm<2>::S2[2] = { NPerm<2>(), NPerm<2>(1) };
const unsigned NPerm<2>::invS2[2] = { 0, 1 };

const NPerm<2>* NPerm<2>::Sn = NPerm<2>::S2;
const unsigned* NPerm<2>::invSn = NPerm<2>::invS2;

const NPerm<2>* NPerm<2>::orderedS2 = NPerm<2>::S2;
const NPerm<2>* NPerm<2>::orderedSn = NPerm<2>::S2;
const NPerm<2>* NPerm<2>::S1 = NPerm<2>::S2;
const NPerm<2>* NPerm<2>::Sn_1 = NPerm<2>::S2;

} // namespace regina

