
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

/*! \file subcomplex/nlayeredloop.h
 *  \brief Deals with layered loop components of a triangulation.
 */

#ifndef __NLAYEREDLOOP_H
#ifndef __DOXYGEN
#define __NLAYEREDLOOP_H
#endif

#include "regina-core.h"
#include "subcomplex/nstandardtri.h"

namespace regina {

template <int, int> class Face;
typedef Face<3, 1> NEdge;

/**
 * \weakgroup subcomplex
 * @{
 */

/**
 * Represents a layered loop component of a triangulation.
 *
 * A layered loop is a layered chain of \a n tetrahedra whose bottom
 * tetrahedron is layered onto its top tetrahedron to form a complete
 * loop.  See the NLayeredChain class notes for a description of a
 * layered chain.
 *
 * To make a layered chain into a layered
 * loop, the bottom faces of the first tetrahedron will be
 * layered upon the top faces of the last tetrahedron, completing the loop.
 * At this stage there is a choice.  The layering can be done in the usual
 * fashion, or there may be a \a twist in which the upper square (the
 * bottom faces of the first tetrahedron) is rotated 180 degrees before
 * being layered on the lower annulus (the top faces of the last
 * tetrahedron).
 *
 * If there is a twist, the two hinge edges become identified and the
 * entire component has a single vertex.  If there is no twist, the
 * two hinge edges remain distinct (and disjoint) and the entire
 * component has two vertices.
 *
 * The \a length of the layered loop is the number of tetrahedra it
 * contains.  A layered loop must contain at least one tetrahedron.
 *
 * All optional NStandardTriangulation routines are implemented for this
 * class.
 */
class REGINA_API NLayeredLoop : public NStandardTriangulation {
    private:
        unsigned long length_;
            /**< The length of this layered loop. */
        NEdge* hinge_[2];
            /**< The hinge edge(s) of this layered loop.  If the loop is
                 twisted, the second element in this array will be \c null. */

    public:
        /**
         * Destroys this layered loop.
         */
        virtual ~NLayeredLoop();
        /**
         * Returns a newly created clone of this structure.
         *
         * @return a newly created clone.
         */
        NLayeredLoop* clone() const;

        /**
         * Returns the length of this layered loop.
         * See the general class notes for further details.
         *
         * @return the length of this layered loop.
         */
        unsigned long length() const;
        /**
         * Deprecated routine that returns the length of this layered loop.
         *
         * \deprecated This routine has been renamed to length().
         * See the length() documentation for further details.
         */
        REGINA_DEPRECATED unsigned long getLength() const;
        /**
         * Returns the length of this layered loop.
         * See the general class notes for further details.
         *
         * \deprecated The preferred way of accessing the length of a
         * layered loop is through length().
         *
         * @return the length of this layered loop.
         */
        REGINA_DEPRECATED unsigned long getIndex() const;
        /**
         * Determines if this layered loop contains a twist.
         * See the general class notes for further details.
         *
         * @return \c true if and only if this layered loop contains a
         * twist.
         */
        bool isTwisted() const;
        /**
         * Returns the requested hinge edge of this layered loop.
         * See the general class notes for further details.
         * If there is only one hinge but parameter \a which is 1,
         * \c null will be returned.
         *
         * @param which specifies which hinge to return; this must be 0
         * or 1.
         * @return the requested hinge edge.
         */
        NEdge* hinge(int which) const;
        /**
         * Deprecated routine that returns the requested hinge edge of this
         * layered loop.
         *
         * \deprecated This routine has been renamed to hinge().
         * See the hinge() documentation for further details.
         */
        REGINA_DEPRECATED NEdge* getHinge(int which) const;

        /**
         * Determines if the given triangulation component is a layered
         * loop.
         *
         * @param comp the triangulation component to examine.
         * @return a newly created structure containing details of the
         * layered loop, or \c null if the given component is
         * not a layered loop.
         */
        static NLayeredLoop* isLayeredLoop(const NComponent* comp);

        NManifold* manifold() const;
        NAbelianGroup* homology() const;
        std::ostream& writeName(std::ostream& out) const;
        std::ostream& writeTeXName(std::ostream& out) const;
        void writeTextLong(std::ostream& out) const;

    private:
        /**
         * Creates a new uninitialised structure.
         */
        NLayeredLoop();
};

/*@}*/

// Inline functions for NLayeredLoop

inline NLayeredLoop::NLayeredLoop() {
}
inline NLayeredLoop::~NLayeredLoop() {
}

inline unsigned long NLayeredLoop::length() const {
    return length_;
}
inline unsigned long NLayeredLoop::getLength() const {
    return length_;
}
inline unsigned long NLayeredLoop::getIndex() const {
    return length_;
}
inline bool NLayeredLoop::isTwisted() const {
    return (hinge_[1] == 0);
}
inline NEdge* NLayeredLoop::hinge(int which) const {
    return hinge_[which];
}
inline NEdge* NLayeredLoop::getHinge(int which) const {
    return hinge_[which];
}
inline std::ostream& NLayeredLoop::writeName(std::ostream& out) const {
    return out << (hinge_[1] ? "C(" : "C~(") << length_ << ')';
}
inline std::ostream& NLayeredLoop::writeTeXName(std::ostream& out) const {
    return out << (hinge_[1] ? "C_{" : "\\tilde{C}_{") << length_ << '}';
}
inline void NLayeredLoop::writeTextLong(std::ostream& out) const {
    out << "Layered loop (" << (hinge_[1] ? "not twisted" : "twisted") <<
        ") of length " << length_;
}

} // namespace regina

#endif

