
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

#include "triangulation/ntriangulation.h"
#include "maths/nmatrixint.h"

namespace regina {

const NAbelianGroup& NTriangulation::homology() const {
    if (H1_.known())
        return *H1_.value();

    if (isEmpty())
        return *(H1_ = new NAbelianGroup());

    // Calculate a maximal forest in the dual 1-skeleton.
    ensureSkeleton();

    // Build a presentation matrix.
    // Each non-boundary not-in-forest triangle is a generator.
    // Each non-boundary edge is a relation.
    unsigned long nBdryEdges = 0;
    for (auto bit = boundaryComponents_.begin();
            bit != boundaryComponents_.end(); bit++) {
        nBdryEdges += (*bit)->countEdges();
    }
    long nGens = countTriangles() - countBoundaryFacets()
        + countComponents() - size();
    long nRels = countEdges() - nBdryEdges;
    NMatrixInt pres(nRels, nGens);

    // Find out which triangle corresponds to which generator.
    long* genIndex = new long[countTriangles()];
    long i = 0;
    for (NTriangle* f : triangles()) {
        if (f->isBoundary() || f->inMaximalForest())
            genIndex[f->index()] = -1;
        else {
            genIndex[f->index()] = i;
            i++;
        }
    }

    // Run through each edge and put the relations in the matrix.
    NTetrahedron* currTet;
    NTriangle* triangle;
    int currTetFace;
    long triGenIndex;
    i = 0;
    for (NEdge* e : edges()) {
        if (! e->isBoundary()) {
            // Put in the relation corresponding to this edge.
            for (auto& emb : *e) {
                currTet = emb.tetrahedron();
                currTetFace = emb.vertices()[2];
                triangle = currTet->triangle(currTetFace);
                triGenIndex = genIndex[triangle->index()];
                if (triGenIndex >= 0) {
                    if ((triangle->front().tetrahedron() == currTet) &&
                            (triangle->front().triangle() == currTetFace))
                        pres.entry(i, triGenIndex) += 1;
                    else
                        pres.entry(i, triGenIndex) -= 1;
                }
            }
            i++;
        }
    }

    delete[] genIndex;

    // Build the group from the presentation matrix and tidy up.
    NAbelianGroup* ans = new NAbelianGroup();
    ans->addGroup(pres);
    return *(H1_ = ans);
}

const NAbelianGroup& NTriangulation::homologyRel() const {
    if (H1Rel_.known())
        return *H1Rel_.value();

    if (countBoundaryComponents() == 0)
        return *(H1Rel_ = new NAbelianGroup(homology()));

    // Calculate the relative first homology wrt the boundary.

    // Find a maximal forest in the 1-skeleton.
    // Note that this will ensure the skeleton has been calculated.
    std::set<NEdge*> forest;
    maximalForestInSkeleton(forest, false);

    // Build a presentation matrix.
    // Each non-boundary not-in-forest edge is a generator.
    // Each non-boundary triangle is a relation.
    unsigned long nBdryVertices = 0;
    unsigned long nBdryEdges = 0;
    unsigned long nClosedComponents = 0;
    for (BoundaryComponentIterator bit = boundaryComponents_.begin();
            bit != boundaryComponents_.end(); bit++) {
        nBdryVertices += (*bit)->countVertices();
        nBdryEdges += (*bit)->countEdges();
    }
    for (ComponentIterator cit = components().begin();
            cit != components().end(); cit++)
        if ((*cit)->isClosed())
            nClosedComponents++;
    long nGens = countEdges() - nBdryEdges
        - countVertices() + nBdryVertices
        + nClosedComponents;
    long nRels = countTriangles() - countBoundaryFacets();
    NMatrixInt pres(nRels, nGens);

    // Find out which edge corresponds to which generator.
    long* genIndex = new long[countEdges()];
    long i = 0;
    for (NEdge* e : edges()) {
        if (e->isBoundary())
            genIndex[e->index()] = -1;
        else if (forest.count(e))
            genIndex[e->index()] = -1;
        else {
            genIndex[e->index()] = i;
            i++;
        }
    }

    // Run through each triangle and put the relations in the matrix.
    NTetrahedron* currTet;
    NPerm4 currTetVertices;
    long edgeGenIndex;
    i = 0;
    int triEdge, currEdgeStart, currEdgeEnd, currEdge;
    for (NTriangle* f : triangles()) {
        if (! f->isBoundary()) {
            // Put in the relation corresponding to this triangle.
            currTet = f->front().tetrahedron();
            currTetVertices = f->front().vertices();
            for (triEdge = 0; triEdge < 3; triEdge++) {
                currEdgeStart = currTetVertices[triEdge];
                currEdgeEnd = currTetVertices[(triEdge + 1) % 3];
                // Examine the edge from vertex edgeStart to edgeEnd
                // in tetrahedron currTet.
                currEdge = NEdge::edgeNumber[currEdgeStart][currEdgeEnd];
                edgeGenIndex = genIndex[currTet->edge(currEdge)->index()];
                if (edgeGenIndex >= 0) {
                    if (currTet->edgeMapping(currEdge)[0] == currEdgeStart)
                        pres.entry(i, edgeGenIndex) += 1;
                    else
                        pres.entry(i, edgeGenIndex) -= 1;
                }
            }
            i++;
        }
    }

    delete[] genIndex;

    // Build the group from the presentation matrix and tidy up.
    NAbelianGroup* ans = new NAbelianGroup();
    ans->addGroup(pres);
    return *(H1Rel_ = ans);
}

const NAbelianGroup& NTriangulation::homologyBdry() const {
    if (H1Bdry_.known())
        return *H1Bdry_.value();

    // Run through the individual boundary components and add the
    // appropriate pieces to the homology group.
    unsigned long rank = 0;
    unsigned long z2rank = 0;

    // Ensure that the skeleton has been calculated.
    ensureSkeleton();

    for (BoundaryComponentIterator bit = boundaryComponents_.begin();
            bit != boundaryComponents_.end(); bit++) {
        if ((*bit)->isOrientable()) {
            rank += (2 - (*bit)->eulerChar());
        } else {
            rank += (1 - (*bit)->eulerChar());
            z2rank++;
        }
    }

    // Build the group and tidy up.
    NAbelianGroup* ans = new NAbelianGroup();
    ans->addRank(rank);
    ans->addTorsionElement(2, z2rank);
    return *(H1Bdry_ = ans);
}

const NAbelianGroup& NTriangulation::homologyH2() const {
    if (H2_.known())
        return *H2_.value();

    if (isEmpty())
        return *(H2_ = new NAbelianGroup());

    // Calculations are different for orientable vs non-orientable
    // components.
    // We know the only components will be Z and Z_2.
    long rank, z2rank;
    if (isOrientable()) {
        // Same as H1Rel without the torsion elements.
        rank = homologyRel().rank();
        z2rank = 0;
    } else {
        // Non-orientable!
        // z2rank = # closed cmpts - # closed orientable cmpts
        z2rank = 0;
        for (auto c : components())
            if (c->isClosed() && (! c->isOrientable()))
                ++z2rank;

        // Find rank(Z_2) + rank(Z) and take off z2rank.
        rank = homologyRel().rank() +
            homologyRel().torsionRank(2) -
            homology().torsionRank(2) -
            z2rank;
    }

    // Build the new group and tidy up.
    NAbelianGroup* ans = new NAbelianGroup();
    ans->addRank(rank);
    if (z2rank)
        ans->addTorsionElement(2, z2rank);
    return *(H2_ = ans);
}

} // namespace regina

