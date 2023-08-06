
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

#include <algorithm>
#include "dim4/dim4edge.h"
#include "dim4/dim4triangulation.h"
#include "hypersurface/nnormalhypersurface.h"
#include "triangulation/ntriangulation.h"
#include "utilities/xmlutils.h"

// Property IDs:
#define PROPID_HS_REALBOUNDARY 5
#define PROPID_HS_COMPACT 6
#define PROPID_HS_SURFACENAME 100

namespace regina {

bool NNormalHypersurfaceVector::isCompact(const Dim4Triangulation* triang)
        const {
    size_t nPents = triang->size();
    size_t pent;
    int type;
    for (pent = 0; pent < nPents; pent++) {
        for (type = 0; type < 5; type++)
            if (tetrahedra(pent, type, triang).isInfinite())
                return false;
        for (type = 0; type < 10; type++)
            if (prisms(pent, type, triang).isInfinite())
                return false;
    }
    return true;
}

NNormalHypersurface::NNormalHypersurface(const Dim4Triangulation* triangulation,
        NNormalHypersurfaceVector* vector) :
        vector_(vector), triangulation_(triangulation) {
}

NNormalHypersurface* NNormalHypersurface::clone() const {
    NNormalHypersurface* ans = new NNormalHypersurface(triangulation_,
        dynamic_cast<NNormalHypersurfaceVector*>(vector_->clone()));

    ans->realBoundary_ = realBoundary_;
    ans->compact_ = compact_;

    return ans;
}

NNormalHypersurface* NNormalHypersurface::doubleHypersurface() const {
    NNormalHypersurface* ans = new NNormalHypersurface(triangulation_,
        dynamic_cast<NNormalHypersurfaceVector*>(vector_->clone()));

    (*(ans->vector_)) *= 2;

    // Some properties can be copied straight across.
    ans->realBoundary_ = realBoundary_;
    ans->compact_ = compact_;

    // And some other properties are best left recalculated.
    return ans;
}

void NNormalHypersurface::writeTextShort(std::ostream& out) const {
    size_t nPents = triangulation_->size();
    size_t pent;
    unsigned j;
    for (pent=0; pent < nPents; pent++) {
        if (pent > 0)
            out << " || ";
        for (j=0; j<5; j++)
            out << tetrahedra(pent, j) << ' ';
        out << ';';
        for (j=0; j<10; j++)
            out << ' ' << prisms(pent, j);
    }
}

void NNormalHypersurface::writeXMLData(std::ostream& out) const {
    using regina::xml::xmlEncodeSpecialChars;
    using regina::xml::xmlValueTag;

    // Write the opening tag including vector length.
    size_t vecLen = vector_->size();
    out << "  <hypersurface len=\"" << vecLen << "\" name=\""
        << xmlEncodeSpecialChars(name_) << "\">";

    // Write all non-zero entries.
    NLargeInteger entry;
    for (size_t i = 0; i < vecLen; i++) {
        entry = (*vector_)[i];
        if (entry != 0)
            out << ' ' << i << ' ' << entry;
    }

    // Write properties.
    if (realBoundary_.known())
        out << "\n\t" << xmlValueTag("realbdry", realBoundary_.value());
    if (compact_.known())
        out << "\n\t" << xmlValueTag("compact", compact_.value());

    // Write the closing tag.
    out << " </hypersurface>\n";
}

bool NNormalHypersurface::isEmpty() const {
    size_t nPents = triangulation_->size();

    size_t p;
    int i;

    for (p = 0; p < nPents; ++p) {
        for (i = 0; i < 5; ++i)
            if (tetrahedra(p, i) != 0)
                return false;

        for (i = 0; i < 10; ++i)
            if (prisms(p, i) != 0)
                return false;
    }

    return true;
}

bool NNormalHypersurface::sameSurface(const NNormalHypersurface& other) const {
    size_t nPents = triangulation_->size();

    size_t p;
    int i;

    for (p = 0; p < nPents; ++p) {
        for (i = 0; i < 5; ++i)
            if (tetrahedra(p, i) != other.tetrahedra(p, i))
                return false;

        for (i = 0; i < 10; ++i)
            if (prisms(p, i) != other.prisms(p, i))
                return false;
    }

    return true;
}

bool NNormalHypersurface::embedded() const {
    size_t nPent = triangulation_->size();

    int type;
    int found, prism[2];
    int i, j;
    for (size_t pent = 0; pent < nPent; ++pent) {
        // Find all prism types that appear in this pentachoron.
        found = 0;
        for (type = 0; type < 10; ++type)
            if (prisms(pent, type) > 0) {
                if (found == 2)
                    return false;
                prism[found++] = type;
            }

        // If we do use two prisms, ensure they are compatible.
        if (found == 2)
            for (i = 0; i < 2; ++i)
                for (j = 0; j < 2; ++j)
                    if (Dim4Edge::edgeVertex[prism[0]][i] ==
                            Dim4Edge::edgeVertex[prism[1]][j])
                        return false;
    }

    return true;
}

bool NNormalHypersurface::locallyCompatible(const NNormalHypersurface& other)
        const {
    size_t nPent = triangulation_->size();

    int type;
    int found, prism[2];
    int i, j;
    for (size_t pent = 0; pent < nPent; ++pent) {
        // Find all prism types that appear in this pentachoron.
        found = 0;
        for (type = 0; type < 10; ++type)
            if (prisms(pent, type) > 0 || other.prisms(pent, type) > 0) {
                if (found == 2)
                    return false;
                prism[found++] = type;
            }

        // If we do use two prisms, ensure they are compatible.
        if (found == 2)
            for (i = 0; i < 2; ++i)
                for (j = 0; j < 2; ++j)
                    if (Dim4Edge::edgeVertex[prism[0]][i] ==
                            Dim4Edge::edgeVertex[prism[1]][j])
                        return false;
    }

    return true;
}

void NNormalHypersurface::calculateRealBoundary() const {
    if (triangulation_->isClosed()) {
        realBoundary_ = false;
        return;
    }

    size_t index;
    size_t tot = triangulation_->size();
    const Dim4Pentachoron* pent;
    int type, facet;

    for (index = 0; index < tot; index++) {
        pent = triangulation_->pentachoron(index);
        if (pent->hasBoundary()) {
            // Check for piece types with boundary
            for (type = 0; type < 10; type++) {
                if (prisms(index, type) > 0) {
                    realBoundary_ = true;
                    return;
                }
            }
            for (type = 0; type < 5; type++)
                if (tetrahedra(index, type) > 0) {
                    // Make sure the tetrahedron actually hits the
                    // boundary.
                    for (facet = 0; facet < 5; facet++) {
                        if (facet == type)
                            continue;
                        if (pent->adjacentPentachoron(facet) == 0) {
                            realBoundary_ = true;
                            return;
                        }
                    }
                }
        }
    }
    realBoundary_ = false;
}

void NNormalHypersurface::calculateFromTriangulation() const {
    orientable_.clear();
    twoSided_.clear();
    connected_.clear();
    H1_.clear();

    NTriangulation* me = triangulate();
    orientable_ = me->isOrientable();
    connected_ = me->isConnected();
    H1_ = new NAbelianGroup(me->homology());
    size_t nComp = me->countComponents();
    delete me;

    NNormalHypersurface* twice = doubleHypersurface();
    NTriangulation* cover = twice->triangulate();
    twoSided_ = (cover->countComponents() == 2 * nComp);
    delete cover;
    delete twice;
}

} // namespace regina

