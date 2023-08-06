
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

#include "file/nglobaldirs.h"
#include "manifold/nsnappeacensusmfd.h"
#include "subcomplex/nsnappeacensustri.h"
#include "triangulation/nexampletriangulation.h"
#include "triangulation/ntriangulation.h"

#include <cstdio>
#include <cstring>

namespace regina {

namespace {
    int homDecode(char c) {
        if (c >= 'a' && c <= 'z')
            return c - 'a';
        if (c >= 'A' && c <= 'Z')
            return c - 'A' + 26;
        return -1;
    }
}

const char NSnapPeaCensusManifold::SEC_5 = 'm';
const char NSnapPeaCensusManifold::SEC_6_OR = 's';
const char NSnapPeaCensusManifold::SEC_6_NOR = 'x';
const char NSnapPeaCensusManifold::SEC_7_OR = 'v';
const char NSnapPeaCensusManifold::SEC_7_NOR = 'y';

NTriangulation* NSnapPeaCensusManifold::construct() const {
    NTriangulation* ans = 0;

    // Hard-code a few special cases so that the numbering of tetrahedra
    // and vertices is compatible with earlier versions of Regina.
    if (section_ == SEC_5) {
        if (index_ == 0) {
            ans = NExampleTriangulation::gieseking();
            ans->setLabel("");
        } else if (index_ == 1) {
            ans = new NTriangulation();
            NTetrahedron* r = ans->newTetrahedron();
            NTetrahedron* s = ans->newTetrahedron();
            r->join(0, s, NPerm4(0, 1, 3, 2));
            r->join(1, s, NPerm4(2, 3, 1, 0));
            r->join(2, s, NPerm4(3, 2, 1, 0));
            r->join(3, s, NPerm4(1, 0, 3, 2));
        } else if (index_ == 2) {
            ans = new NTriangulation();
            NTetrahedron* r = ans->newTetrahedron();
            NTetrahedron* s = ans->newTetrahedron();
            r->join(0, s, NPerm4(0, 1, 3, 2));
            r->join(1, s, NPerm4(3, 1, 2, 0));
            r->join(2, s, NPerm4(2, 1, 3, 0));
            r->join(3, s, NPerm4(3, 1, 0, 2));
        } else if (index_ == 3) {
            ans = new NTriangulation();
            NTetrahedron* r = ans->newTetrahedron();
            NTetrahedron* s = ans->newTetrahedron();
            r->join(0, s, NPerm4(0, 1, 3, 2));
            r->join(1, s, NPerm4(2, 1, 0, 3));
            r->join(2, s, NPerm4(0, 3, 2, 1));
            r->join(3, s, NPerm4(1, 0, 2, 3));
        } else if (index_ == 4) {
            ans = NExampleTriangulation::figureEight();
            ans->setLabel("");
        } else if (index_ == 129) {
            ans = NExampleTriangulation::whiteheadLink();
            ans->setLabel("");
        }
    }
    if (ans)
        return ans;

    // Fetch the relevant data from the census dehydration files.
    std::string file = NGlobalDirs::data() + "/snappea";
    switch (section_) {
        case SEC_5:
            file += "/snappea-census-sec5.dat"; break;
        case SEC_6_OR:
            file += "/snappea-census-sec6o.dat"; break;
        case SEC_6_NOR:
            file += "/snappea-census-sec6n.dat"; break;
        case SEC_7_OR:
            file += "/snappea-census-sec7o.dat"; break;
        case SEC_7_NOR:
            file += "/snappea-census-sec7n.dat"; break;
        default:
            return 0;
    }

    FILE* dat = fopen(file.c_str(), "r");
    if (! dat) {
        std::cerr << "Cannot open data file: " << file << std::endl;
        return 0;
    }
    char tri[30], hom[30]; /* Long enough to deal with the snappea census
                              files for <= 7 tetrahedra. */
    for (unsigned i = 0; i <= index_; ++i) {
        if (fscanf(dat, "%s%s", tri, hom) != 2) {
            if (feof(dat))
                std::cerr << "Read beyond end of data file: "
                    << file << std::endl;
            else
                std::cerr << "Error reading data file: " << file << std::endl;
            return 0;
        }
    }
    fclose(dat);

    ans = NTriangulation::rehydrate(tri);
    return ans;
}

NAbelianGroup* NSnapPeaCensusManifold::homology() const {
    // Fetch the relevant data from the census dehydration files.
    std::string file = NGlobalDirs::data() + "/snappea";
    switch (section_) {
        case SEC_5:
            file += "/snappea-census-sec5.dat"; break;
        case SEC_6_OR:
            file += "/snappea-census-sec6o.dat"; break;
        case SEC_6_NOR:
            file += "/snappea-census-sec6n.dat"; break;
        case SEC_7_OR:
            file += "/snappea-census-sec7o.dat"; break;
        case SEC_7_NOR:
            file += "/snappea-census-sec7n.dat"; break;
        default:
            return 0;
    }

    FILE* dat = fopen(file.c_str(), "r");
    if (! dat) {
        std::cerr << "Cannot open data file: " << file << std::endl;
        return 0;
    }
    char tri[30], hom[30]; /* Long enough to deal with the snappea census
                              files for <= 7 tetrahedra. */
    for (unsigned i = 0; i <= index_; ++i) {
        if (fscanf(dat, "%s%s", tri, hom) != 2) {
            if (feof(dat))
                std::cerr << "Read beyond end of data file: "
                    << file << std::endl;
            else
                std::cerr << "Error reading data file: " << file << std::endl;
            return 0;
        }
    }
    fclose(dat);

    NAbelianGroup* ans = new NAbelianGroup();
    char* c;
    int val;

    // First character of the homology string represents rank.
    val = homDecode(hom[0]); // Empty string is picked up and dealt with here.
    if (val < 0) {
        delete ans;
        return 0;
    }
    ans->addRank(val);

    // The remaining characters represent torsion.
    std::multiset<NLargeInteger> torsion;
    for (c = hom + 1; *c; ++c) {
        val = homDecode(*c);
        if (val < 0) {
            delete ans;
            return 0;
        }
        torsion.insert(val);
    }
    ans->addTorsionElements(torsion);
    return ans;
}

std::ostream& NSnapPeaCensusManifold::writeName(std::ostream& out) const {
    // Some manifolds will get special names, and will have their usual
    // SnapPea names written in writeStructure() instead.
    if (section_ == SEC_5) {
        if (index_ == 0)
            return out << "Gieseking manifold";
        if (index_ == 4)
            return out << "Figure eight knot complement";
        if (index_ == 129)
            return out << "Whitehead link complement";
    }

    // No special names, just the usual SnapPea notation.
    return NSnapPeaCensusTri(section_, index_).writeName(out);
}

std::ostream& NSnapPeaCensusManifold::writeTeXName(std::ostream& out) const {
    return NSnapPeaCensusTri(section_, index_).writeTeXName(out);
}

std::ostream& NSnapPeaCensusManifold::writeStructure(std::ostream& out) const {
    // If we didn't give the usual SnapPea name in writeName(), give it here.
    if (section_ == SEC_5) {
        if (index_ == 0 || index_ == 4 || index_ == 129)
            return NSnapPeaCensusTri(section_, index_).writeName(out);
    }

    return out;
}

} // namespace regina

