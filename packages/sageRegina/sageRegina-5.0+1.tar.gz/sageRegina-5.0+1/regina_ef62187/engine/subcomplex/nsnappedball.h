
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

/*! \file subcomplex/nsnappedball.h
 *  \brief Deals with snapped 3-balls in a triangulation.
 */

#ifndef __NSNAPPEDBALL_H
#ifndef __DOXYGEN
#define __NSNAPPEDBALL_H
#endif

#include "regina-core.h"
#include "subcomplex/nstandardtri.h"
#include "triangulation/nedge.h"

namespace regina {

template <int> class Simplex;
typedef Simplex<3> NTetrahedron;

/**
 * \weakgroup subcomplex
 * @{
 */

/**
 * Represents a snapped 3-ball in a triangulation.
 * A snapped 3-ball is a single tetrahedron with two faces glued to each
 * other to form a 3-ball with a two triangle boundary.
 *
 * All optional NStandardTriangulation routines are implemented for this
 * class.
 */
class REGINA_API NSnappedBall : public NStandardTriangulation {
    private:
        NTetrahedron* tet;
            /**< The tetrahedron that forms the snapped ball. */
        int equator;
            /**< The edge that forms the equator on the ball boundary. */

    public:
        /**
         * Returns a newly created clone of this structure.
         *
         * @return a newly created clone.
         */
        NSnappedBall* clone() const;

        /**
         * Returns the tetrahedron that forms this snapped ball.
         *
         * @return the tetrahedron.
         */
        NTetrahedron* tetrahedron() const;
        /**
         * Deprecated routine that returns the tetrahedron that forms this
         * snapped ball.
         *
         * \deprecated This routine has been renamed to tetrahedron().
         * See the tetrahedron() documentation for further details.
         */
        REGINA_DEPRECATED NTetrahedron* getTetrahedron() const;

        /**
         * Returns one of the two tetrahedron faces that forms the boundary
         * of this snapped ball.
         *
         * You are guaranteed that index 0 will return a smaller face
         * number than index 1.
         *
         * @param index specifies which of the two boundary faces to return;
         * this must be either 0 or 1.
         * @return the corresponding face number in the tetrahedron.
         */
        int boundaryFace(int index) const;
        /**
         * Deprecated routine that returns one of the two tetrahedron faces
         * that forms the boundary of this snapped ball.
         *
         * \deprecated This routine has been renamed to boundaryFace().
         * See the boundaryFace() documentation for further details.
         */
        REGINA_DEPRECATED int getBoundaryFace(int index) const;
        /**
         * Returns one of the two tetrahedron faces internal to this snapped
         * ball.
         *
         * You are guaranteed that index 0 will return a smaller face
         * number than index 1.
         *
         * @param index specifies which of the two internal faces to return;
         * this must be either 0 or 1.
         * @return the corresponding face number in the tetrahedron.
         */
        int internalFace(int index) const;
        /**
         * Deprecated routine that returns one of the two tetrahedron faces
         * internal to this snapped ball.
         *
         * \deprecated This routine has been renamed to internalFace().
         * See the internalFace() documentation for further details.
         */
        REGINA_DEPRECATED int getInternalFace(int index) const;
        /**
         * Returns the edge that forms the equator of the boundary sphere
         * of this ball.
         *
         * @return the corresponding edge number in the tetrahedron.
         */
        int equatorEdge() const;
        /**
         * Deprecated routine that returns the edge that forms the equator of
         * the boundary sphere of this ball.
         *
         * \deprecated This routine has been renamed to equatoryEdge().
         * See the equatorEdge() documentation for further details.
         */
        REGINA_DEPRECATED int getEquatorEdge() const;
        /**
         * Returns the edge internal to this snapped ball.
         *
         * @return the corresponding edge number in the tetrahedron.
         */
        int internalEdge() const;
        /**
         * Deprecated routine that returns the edge internal to this snapped
         * ball.
         *
         *
         * \deprecated This routine has been renamed to internalEdge().
         * See the internalEdge() documentation for further details.
         */
        REGINA_DEPRECATED int getInternalEdge() const;

        /**
         * Determines if the given tetrahedron forms a snapped 3-ball
         * within a triangulation.  The ball need not be the entire
         * triangulation; the boundary triangles may be glued to something
         * else (or to each other).
         *
         * Note that the two boundary triangles of the snapped 3-ball
         * need not be boundary triangles within the overall
         * triangulation, i.e., they may be identified with each other
         * or with triangles of other tetrahedra.
         *
         * @param tet the tetrahedron to examine as a potential 3-ball.
         * @return a newly created structure containing details of the
         * snapped 3-ball, or \c null if the given tetrahedron is
         * not a snapped 3-ball.
         */
        static NSnappedBall* formsSnappedBall(NTetrahedron* tet);

        NManifold* manifold() const;
        NAbelianGroup* homology() const;
        std::ostream& writeName(std::ostream& out) const;
        std::ostream& writeTeXName(std::ostream& out) const;
        void writeTextLong(std::ostream& out) const;

    private:
        /**
         * Creates a new uninitialised structure.
         */
        NSnappedBall();
};

/*@}*/

// Inline functions for NSnappedBall

inline NSnappedBall::NSnappedBall() {
}
inline NTetrahedron* NSnappedBall::tetrahedron() const {
    return tet;
}
inline NTetrahedron* NSnappedBall::getTetrahedron() const {
    return tet;
}
inline int NSnappedBall::boundaryFace(int index) const {
    return index == 0 ?
        NEdge::edgeVertex[5 - equator][0] :
        NEdge::edgeVertex[5 - equator][1];
}
inline int NSnappedBall::getBoundaryFace(int index) const {
    return index == 0 ?
        NEdge::edgeVertex[5 - equator][0] :
        NEdge::edgeVertex[5 - equator][1];
}
inline int NSnappedBall::internalFace(int index) const {
    return index == 0 ?
        NEdge::edgeVertex[equator][0] :
        NEdge::edgeVertex[equator][1];
}
inline int NSnappedBall::getInternalFace(int index) const {
    return index == 0 ?
        NEdge::edgeVertex[equator][0] :
        NEdge::edgeVertex[equator][1];
}
inline int NSnappedBall::equatorEdge() const {
    return equator;
}
inline int NSnappedBall::getEquatorEdge() const {
    return equator;
}
inline int NSnappedBall::internalEdge() const {
    return 5 - equator;
}
inline int NSnappedBall::getInternalEdge() const {
    return 5 - equator;
}
inline std::ostream& NSnappedBall::writeName(std::ostream& out) const {
    return out << "Snap";
}
inline std::ostream& NSnappedBall::writeTeXName(std::ostream& out) const {
    return out << "\\mathit{Snap}";
}
inline void NSnappedBall::writeTextLong(std::ostream& out) const {
    out << "Snapped 3-ball";
}

} // namespace regina

#endif

