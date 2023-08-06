
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

/*! \file surfaces/nnormalsurface.h
 *  \brief Deals with an individual normal surface in a 3-manifold
 *  triangulation.
 */

#ifndef __NNORMALSURFACE_H
#ifndef __DOXYGEN
#define __NNORMALSURFACE_H
#endif

#include <utility>
#include "regina-core.h"
#include "output.h"
#include "maths/nperm4.h"
#include "maths/nray.h"
#include "surfaces/ndisctype.h"
#include "surfaces/normalcoords.h"
#include "utilities/nbooleans.h"
#include "utilities/nproperty.h"
#include <boost/noncopyable.hpp>

namespace regina {

/**
 * \addtogroup surfaces Normal Surfaces
 * Normal surfaces in 3-manifold triangulations.
 * @{
 */

/**
 * Lists which quadrilateral types separate which pairs of vertices in a
 * tetrahedron.
 * As outlined in NNormalSurface::quads(), there are three quadrilateral types
 * in a tetrahedron, numbered 0, 1 and 2.  Each quadrilateral type separates
 * the four tetrahedron vertices 0,1,2,3 into two pairs.
 * <tt>quadSeparating[i][j]</tt> is the number of the quadrilateral type that
 * keeps vertices <tt>i</tt> and <tt>j</tt> together.
 *
 * It is guaranteed that quadrilateral type \a i will keep the vertices of
 * edge \a i together (and will therefore also keep the vertices of edge
 * \a 5-i together).
 */
REGINA_API extern const int quadSeparating[4][4];
/**
 * Deprecated alias for regina::quadSeparating.
 *
 * \deprecated This array has been renamed to regina::quadSeparating.
 * See the regina::quadSeparating documentation for further details.
 */
REGINA_DEPRECATED REGINA_API extern const int (*vertexSplit)[4];
/**
 * Lists which quadrilateral types meet which edges in a tetrahedron.
 * See regina::quadSeparating and NNormalSurface::quads() for more
 * information on quadrilateral types.
 *
 * <tt>quadMeeting[i][j][0,1]</tt> are the numbers of the two
 * quadrilateral types that meet the edge joining tetrahedron vertices
 * <tt>i</tt> and <tt>j</tt>.
 */
REGINA_API extern const int quadMeeting[4][4][2];
/**
 * Deprecated alias for regina::quadMeeting.
 *
 * \deprecated This array has been renamed to regina::quadMeeting.
 * See the regina::quadMeeting documentation for further details.
 */
REGINA_DEPRECATED REGINA_API extern const int (*vertexSplitMeeting)[4][2];

/**
 * Deprecated array that lists the vertices which each quadrilateral type
 * separates within a tetrahedron.
 * See regina::quadSeparating and NNormalSurface::quads() for more
 * information on quadrilateral types.
 *
 * Quadrilateral type \c i splits the vertex pairs
 * <tt>vertexSplitDefn[i][0,1]</tt> and
 * <tt>vertexSplitDefn[i][2,3]</tt>.
 *
 * It is guaranteed that:
 *
 * - <tt>vertexSplitDefn[i][0] < vertexSplitDefn[i][1]</tt>;
 *
 * - <tt>vertexSplitDefn[i][2] < vertexSplitDefn[i][3]</tt>;
 *
 * - <tt>vertexSplitDefn[i][0] < vertexSplitDefn[i][2]</tt>.
 *
 * \deprecated This array is redundant, and will be removed in a future
 * release of Regina.  Instead of vertexSplitDefn[\a i][\a j], you can
 * call NEdge::ordering(\a i)[\a j] which carries the same information.
 * Be aware however that NEdge::ordering() might reorder the images
 * NEdge::ordering(\a i)[2] and NEdge::ordering(\a i)[3].
 */
REGINA_DEPRECATED REGINA_API extern const int vertexSplitDefn[3][4];

/**
 * Lists the second vertex with which each vertex is paired under each
 * quadrilateral type in a tetrahedron.
 * See regina::quadSeparating and NNormalSurface::quads() for more
 * information on quadrilateral types.
 *
 * Quadrilateral type \c i pairs vertex \c v with
 * vertex <tt>quadPartner[i][v]</tt>.
 */
REGINA_API extern const int quadPartner[3][4];
/**
 * Deprecated alias for regina::quadPartner.
 *
 * \deprecated This array has been renamed to regina::quadPartner.
 * See the regina::quadPartner documentation for further details.
 */
REGINA_DEPRECATED REGINA_API extern const int (*vertexSplitPartner)[4];

/**
 * Contains strings that can be used to represent each quadrilateral type
 * in a tetrahedron.
 * See regina::quadSeparating and NNormalSurface::quads() for more
 * information on quadrilateral types.
 *
 * The string describing quadrilateral type \c i is <tt>quadString[i]</tt> and
 * is of the form <tt>02/13</tt>, which in this case is the quadrilateral type
 * that splits vertices 0,2 from vertices 1,3.
 */
REGINA_API extern const char quadString[3][6];
/**
 * Deprecated alias for regina::quadString.
 *
 * \deprecated This array has been renamed to regina::quadString.
 * See the regina::quadString documentation for further details.
 */
REGINA_DEPRECATED REGINA_API extern const char (*vertexSplitString)[6];

/**
 * Lists in consecutive order the directed normal arcs that form the
 * boundary of each type of triangular normal disc.  Each permutation \a p
 * represents an arc about vertex <tt>p[0]</tt> parallel to the directed
 * edge from <tt>p[1]</tt> to <tt>p[2]</tt>.
 *
 * Array <tt>triDiscArcs[i]</tt> lists the boundary arcs of the
 * triangular disc of type <i>i</i>.  See NNormalSurface::triangles()
 * for further details.
 *
 * Note that every permutation in this array is even.
 *
 * \ifacescpp This array is replaced by a macro
 * <tt>triDiscArcs(discType, arcIndex)</tt> that essentially looks up
 * the corresponding array.  This is necessary because of a bug in gcc 2.95.
 */
#ifdef __DOXYGEN
REGINA_API extern const NPerm4 triDiscArcs[4][3];
#else
REGINA_API extern const NPerm4 __triDiscArcs[12];
#define triDiscArcs(i, j) __triDiscArcs[(3 * (i)) + (j)]
#endif

/**
 * Lists in consecutive order the directed normal arcs that form the
 * boundary of each type of quadrilateral normal disc.  Each permutation \a p
 * represents an arc about vertex <tt>p[0]</tt> parallel to the directed
 * edge from <tt>p[1]</tt> to <tt>p[2]</tt>.
 *
 * Array <tt>quadDiscArcs[i]</tt> lists the boundary arcs of the
 * quadrilateral disc of type <i>i</i>.  See NNormalSurface::quads()
 * for further details.
 *
 * Note that permutation <tt>quadDiscArcs[i][j]</tt> will be even
 * precisely when <tt>j</tt> is even.
 *
 * \ifacescpp This array is replaced by a macro
 * <tt>quadDiscArcs(discType, arcIndex)</tt> that essentially looks up
 * the corresponding array.  This is necessary because of a bug in gcc 2.95.
 */
#ifdef __DOXYGEN
REGINA_API extern const NPerm4 quadDiscArcs[3][4];
#else
REGINA_API extern const NPerm4 __quadDiscArcs[12];
#define quadDiscArcs(i, j) __quadDiscArcs[(4 * (i)) + (j)]
#endif

/**
 * Lists in consecutive order the directed normal arcs that form the
 * boundary of each type of octagonal normal disc.  Each permutation \a p
 * represents an arc about vertex <tt>p[0]</tt> parallel to the directed
 * edge from <tt>p[1]</tt> to <tt>p[2]</tt>.
 *
 * Array <tt>octDiscArcs[i]</tt> lists the boundary arcs of the
 * octagonal disc of type <i>i</i>.  See NNormalSurface::octs()
 * for further details.
 *
 * Note that permutation <tt>octDiscArcs[i][j]</tt> will be even
 * precisely when <tt>j</tt> is 0, 1, 4 or 5.
 *
 * \ifacescpp This array is replaced by a macro
 * <tt>octDiscArcs(discType, arcIndex)</tt> that essentially looks up
 * the corresponding array.  This is necessary because of a bug in gcc 2.95.
 */
#ifdef __DOXYGEN
REGINA_API extern const NPerm4 octDiscArcs[3][8];
#else
REGINA_API extern const NPerm4 __octDiscArcs[24];
#define octDiscArcs(i, j) __octDiscArcs[(8 * (i)) + (j)]
#endif

class NEnumConstraintList;
class NXMLNormalSurfaceReader;
class NMatrixInt;

template <int> class Triangulation;
template <int, int> class Face;
typedef Triangulation<3> NTriangulation;
typedef Face<3, 0> NVertex;
typedef Face<3, 1> NEdge;

/**
 * A template that stores information about a particular
 * normal coordinate system.  Much of this information is given in the
 * form of compile-time constants and types.
 *
 * To iterate through cases for a given value of NormalCoords that is not
 * known until runtime, see the various forCoords() routines defined in
 * coordregistry.h.
 *
 * This NormalInfo template should only be defined for \a coordType
 * arguments that represent coordinate systems in which you can create and
 * store normal surfaces.
 *
 * At a bare minimum, each specialisation of this template must provide:
 *
 * - a typedef \a Class that represents the corresponding
 *   NNormalSurfaceVector subclass;
 * - typedefs \a Standard and \a Reduced that identify NormalInfo templates
 *   for the corresponding coordinate systems with and without triangles
 *   (if this is not meaningful then both typedefs should just identify this
 *   system);
 * - enum constants \a almostNormal, \a spun and \a oriented, which indicate
 *   whether the coordinate system allows almost normal, spun and/or
 *   transversely oriented surfaces;
 * - a static function name() that returns a C-style string giving the
 *   human-readable name of the coordinate system.
 *
 * \ifacespython Not present.
 *
 * \tparam coordType one of the #NormalCoords constants, indicating
 * which coordinate system we are querying.
 */
template <NormalCoords coordType>
struct NormalInfo;

/**
 * Defines various constants, types and virtual functions for a subclass
 * of NNormalSurfaceVector.
 *
 * Every subclass of NNormalSurfaceVector \a must include
 * REGINA_NORMAL_SURFACE_FLAVOUR at the beginning of the class definition.
 *
 * This macro provides the class with:
 *
 * - a compile-time constant \a coordsID and a deprecated compile-time constant
 *   \a coordType, both equal to the corresponding NormalCoords constant;
 * - a typedef \a Info, which refers to the corresponding specialisation
 *   of the NormalInfo<> template;
 * - declarations and implementations of the virtual functions
 *   NNormalSurfaceVector::clone(),
 *   NNormalSurfaceVector::allowsAlmostNormal(),
 *   NNormalSurfaceVector::allowsSpun(), and
 *   NNormalSurfaceVector::allowsOriented().
 *
 * @param class_ the name of this subclass of NNormalSurfaceVector.
 * @param id the corresponding NNormalCoords constant.
 */
#define REGINA_NORMAL_SURFACE_FLAVOUR(class_, id) \
    public: \
        typedef NormalInfo<id> Info; \
        static constexpr const NormalCoords coordsID = id; \
        REGINA_DEPRECATED static constexpr const NormalCoords coordType = id; \
        inline virtual NNormalSurfaceVector* clone() const { \
            return new class_(*this); \
        } \
        inline virtual bool allowsAlmostNormal() const { \
            return Info::almostNormal; \
        } \
        inline virtual bool allowsSpun() const { \
            return Info::spun; \
        } \
        inline virtual bool allowsOriented() const { \
            return Info::oriented; \
        }

/**
 * Stores the vector of a single normal surface in a 3-manifold.
 * The different subclasses of NNormalSurfaceVector use different
 * underlying coordinate systems for the normal solution space.
 * However, the various coordinate retrieval routines will return values
 * that are independent of the underlying coordinate system.  Thus the
 * coordinates of the normal surface in any coordinate system can be
 * determined without knowledge of the specific underlying coordinate
 * system being used.
 *
 * Note that if a mirrored vector class is being used (see
 * NNormalSurfaceVectorMirrored), the vector <b>may not change</b> once
 * the first coordinate lookup routine (such as triangles() and
 * the like) has been called.  See
 * NNormalSurfaceVectorMirrored for further explanation.
 *
 * Note that non-compact surfaces (surfaces with infinitely many discs,
 * such as spun-normal surfaces) are allowed; in these cases, the
 * corresponding coordinate lookup routines should return
 * NLargeInteger::infinity where appropriate.
 *
 * All subclasses of NNormalSurfaceVector <b>must</b> have the following
 * properties:
 *
 * - Normal surfaces can be enumerated by intersecting the non-negative
 *   orthant of the underlying vector space with some linear subspace;
 *
 * - Multiplying a normal surface by \a k corresponds to multiplying
 *   the underlying vector by \a k for any non-negative integer \a k.
 *
 * <b>When deriving classes from NNormalSurfaceVector:</b>
 * <ul>
 *   <li>A new value must must be added to the NormalCoords enum in
 *   normalcoords.h to represent the new coordinate system.</li>
 *   <li>The file coordregistry-impl.h must be updated to reflect the new
 *   coordinate system (the file itself contains instructions
 *   on how to do this).</li>
 *   <li>A corresponding specialisation of NormalInfo<> must be
 *   defined, typically in the same header as the new vector subclass.</li>
 *   <li>The macro REGINA_NORMAL_SURFACE_FLAVOUR must be added to the
 *   beginning of the new vector subclass.  This will declare and define
 *   various constants, typedefs and virtual functions (see the
 *   REGINA_NORMAL_SURFACE_FLAVOUR macro documentation for details).</li>
 *   <li>Constructors <tt>class(size_t length)</tt> and
 *   <tt>class(const NVector<NLargeInteger>& cloneMe)</tt> must be
 *   declared and implemented; these will usually just call the
 *   corresponding superclass constructors.</li>
 *   <li>All abstract functions must be implemented, except for those
 *   already provided by REGINA_NORMAL_SURFACE_FLAVOUR.
 *   Note that coordinate functions such as triangles() must return the
 *   \e total number of discs of the requested type; if your new coordinate
 *   system adorns discs with extra information (such as orientation) then
 *   your implementation must compute the appropriate sum.</li>
 *   <li>The orientation-specific coordinate functions
 *   orientedTriangles() and orientedQuads() must be
 *   implemented if your coordinate system supports transverse orientation.
 *   Otherwise you can use the default implementations (which returns zero).
 *   <li>Static public functions <tt>void
 *   makeZeroVector(const NTriangulation*)</tt>,
 *   <tt>NMatrixInt* makeMatchingEquations(const NTriangulation*)</tt> and
 *   makeEmbeddedConstraints(const NTriangulation*) must be
 *   declared and implemented.</li>
 * </ul>
 *
 * \todo \optlong Investigate using sparse vectors for storage.
 *
 * \ifacespython Not present.
 */
class REGINA_API NNormalSurfaceVector : public NRay {
    public:
        /**
         * Creates a new vector all of whose entries are initialised to
         * zero.
         *
         * @param length the number of elements in the new vector.
         */
        NNormalSurfaceVector(size_t length);
        /**
         * Creates a new vector that is a clone of the given vector.
         *
         * @param cloneMe the vector to clone.
         */
        NNormalSurfaceVector(const NVector<NLargeInteger>& cloneMe);

        /**
         * A virtual destructor.  This is required because here we introduce
         * virtual functions into the NRay hierarchy.
         */
        virtual ~NNormalSurfaceVector();

        /**
         * Creates a newly allocated clone of this vector.
         * The clone will be of the same subclass of NNormalSurfaceVector
         * as this vector.
         */
        virtual NNormalSurfaceVector* clone() const = 0;

        /**
         * Determines if the specific underlying coordinate system
         * allows for almost normal surfaces, that is, allows for
         * octagonal discs.
         *
         * Note that this has nothing to do with whether or not this
         * specific surface \e contains octagonal discs.
         *
         * @return \c true if and only if almost normal surfaces are allowed.
         */
        virtual bool allowsAlmostNormal() const = 0;

        /**
         * Determines if the specific underlying coordinate system
         * allows for spun-normal surfaces; that is, surfaces with
         * infinitely many triangles.
         *
         * Note that this has nothing to do with whether or not this
         * specific surface \e contains infinitely many triangles.
         *
         * @return \c true if and only if spun-normal surfaces are allowed.
         */
        virtual bool allowsSpun() const = 0;

        /**
         * Determines if the specific underlying coordinate system
         * allows for transversely oriented normal surfaces.
         *
         * @return \c true if and only if transverse orientations are
         * supported.
         */
        virtual bool allowsOriented() const = 0;

        /**
         * Determines if this normal surface has more than one
         * octagonal disc.  It may be assumed that at most one
         * octagonal disc \e type exists in this surface.  This routine will
         * return \c true if an octagonal type does exist and its
         * coordinate is greater than one.
         *
         * The default implementation for this routine simply calculates
         * all the octagonal coordinates and returns as soon as a
         * positive or negative result can be established.  Subclasses
         * of NNormalSurfaceVector should override this if they can provide a
         * faster implementation.
         *
         * If a subclass does not allow for almost normal surfaces, this
         * routine will never be called and thus does not need to be
         * overwritten.
         *
         * \pre At most one octagonal disc \e type exists in this surface.
         * \pre This normal surface vector is using a
         * coordinate system that allows for almost normal surfaces.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return \c true if and only if there is an octagonal disc type
         * present and its coordinate is greater than one.
         */
        virtual bool hasMultipleOctDiscs(const NTriangulation* triang) const;
        /**
         * Determines if the normal surface represented is compact (has
         * finitely many discs).
         *
         * The default implementation for this routine simply runs
         * through every disc type until a disc type with infinite disc
         * count is found or all disc types have been examined.
         * Subclasses of NNormalSurfaceVector should override this if
         * they can provide a faster implementation.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return \c true if and only if the normal surface represented
         * is compact.
         */
        virtual bool isCompact(const NTriangulation* triang) const;
        /**
         * Determines if the normal surface represented is vertex
         * linking.  A <i>vertex linking</i> surface contains only
         * triangles.
         *
         * The default implementation for this routine simply runs
         * through every non-triangular disc type ensuring that each
         * has no corresponding discs.
         * Subclasses of NNormalSurfaceVector should override this if
         * they can provide a faster implementation.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return \c true if and only if the normal surface represented
         * is vertex linking.
         */
        virtual bool isVertexLinking(const NTriangulation* triang) const;
        /**
         * Determines if a rational multiple of the normal surface represented
         * is the link of a single vertex.
         *
         * The default implementation for this routine involves counting the
         * number of discs of every type.
         * Subclasses of NNormalSurfaceVector should override this if
         * they can provide a faster implementation.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return the vertex linked by this surface, or 0 if this
         * surface is not the link of a single vertex.
         */
        virtual const NVertex* isVertexLink(const NTriangulation* triang) const;
        /**
         * Determines if a rational multiple of the normal surface represented
         * is the thin link of a single edge.
         *
         * If there are two different edges <i>e1</i> and <i>e2</i> for
         * which the surface could be expressed as the thin link of
         * either <i>e1</i> or <i>e2</i>, the pair
         * (<i>e1</i>,<i>e2</i>) will be returned.
         * If the surface is the thin link of only one edge <i>e</i>,
         * the pair (<i>e</i>,0) will be returned.
         * If the surface is not the thin link of any edges, the pair
         * (0,0) will be returned.
         *
         * The default implementation for this routine involves counting the
         * number of discs of every type.
         * Subclasses of NNormalSurfaceVector should override this if
         * they can provide a faster implementation.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return a pair containing the edge(s) linked by this surface,
         * as described above.
         */
        virtual std::pair<const NEdge*, const NEdge*> isThinEdgeLink(
            const NTriangulation* triang) const;
        /**
         * Determines if the normal surface represented is a splitting
         * surface in the given triangulation.  A \a splitting surface
         * is a compact surface containing precisely
         * one quad per tetrahedron and no other normal (or almost
         * normal) discs.
         *
         * The default implementation for this routine simply runs
         * through and checks the count for each disc type.
         * Subclasses of NNormalSurfaceVector should override this if
         * they can provide a faster implementation.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return \c true if and only if the normal surface represented
         * is a splitting surface.
         */
        virtual bool isSplitting(const NTriangulation* triang) const;
        /**
         * Determines if the normal surface represented is a central
         * surface in the given triangulation.  A \a central surface
         * is a compact surface containing at most one normal or almost
         * normal disc per tetrahedron.  If the surface is central, the
         * number of tetrahedra it meets (i.e., the number of discs in
         * the surface) will be returned.
         *
         * The default implementation for this routine simply runs
         * through and checks the count for each disc type.
         * Subclasses of NNormalSurfaceVector should override this if
         * they can provide a faster implementation.
         *
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of tetrahedra that the surface meets if it
         * is a central surface, or 0 if it is not a central surface.
         */
        virtual NLargeInteger isCentral(const NTriangulation* triang) const;

        /**
         * Returns the number of triangular discs of the given type in
         * this normal surface.
         * See NNormalSurface::triangles() for further details.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested triangles reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param vertex the vertex of the given tetrahedron around
         * which the requested triangles lie; this should be between 0
         * and 3 inclusive.
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of triangular discs of the given type.
         */
        virtual NLargeInteger triangles(size_t tetIndex,
            int vertex, const NTriangulation* triang) const = 0;
        /**
         * Deprecated routine that returns the number of triangular discs
         * of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to triangles().
         * See the triangles() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getTriangleCoord(size_t tetIndex,
            int vertex, const NTriangulation* triang) const;

        /**
         * Returns the number of oriented triangular discs of the given type in
         * this normal surface.
         * See NNormalSurface::orientedTriangles() for further details.
         *
         * The default implementation of this routine returns zero,
         * which is suitable for coordinate systems that do not support
         * transverse orientation.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested triangles reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param vertex the vertex of the given tetrahedron around
         * which the requested triangles lie; this should be between 0
         * and 3 inclusive.
         * @param triang the triangulation in which this normal surface lives.
         * @param orientation the orientation of the normal discs.
         * @return the number of triangular discs of the given type.
         */
        virtual NLargeInteger orientedTriangles(size_t tetIndex,
            int vertex, const NTriangulation* triang, bool orientation) const;
        /**
         * Deprecated routine that returns the number of oriented
         * triangular discs of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to orientedTriangles().
         * See the orientedTriangles() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getOrientedTriangleCoord(
            size_t tetIndex, int vertex, const NTriangulation* triang,
            bool orientation) const;

        /**
         * Returns the number of quadrilateral discs of the given type
         * in this normal surface.
         * See NNormalSurface::quads() for further details.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested quadrilaterals reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param quadType the type of this quadrilateral in the given
         * tetrahedron; this should be 0, 1 or 2.
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of quadrilateral discs of the given type.
         */
        virtual NLargeInteger quads(size_t tetIndex,
            int quadType, const NTriangulation* triang) const = 0;
        /**
         * Deprecated routine that returns the number of quadrilateral discs
         * of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to quads().
         * See the quads() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getQuadCoord(size_t tetIndex,
            int quadType, const NTriangulation* triang) const;

        /**
         * Returns the number of oriented quadrilateral discs of the given type
         * in this normal surface.
         * See NNormalSurface::orientedQuads() for further details.
         *
         * The default implementation of this routine returns zero,
         * which is suitable for coordinate systems that do not support
         * transverse orientation.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested quadrilaterals reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param quadType the type of this quadrilateral in the given
         * tetrahedron; this should be 0, 1 or 2.
         * @param triang the triangulation in which this normal surface lives.
         * @param orientation the orientation of the normal discs.
         * @return the number of quadrilateral discs of the given type.
         */
        virtual NLargeInteger orientedQuads(size_t tetIndex,
            int quadType, const NTriangulation* triang, bool orientation) const;
        /**
         * Deprecated routine that returns the number of oriented
         * quadrilateral discs of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to orientedQuads().
         * See the orientedQuads() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getOrientedQuadCoord(size_t tetIndex,
            int quadType, const NTriangulation* triang, bool orientation) const;
        /**
         * Returns the number of octagonal discs of the given type
         * in this normal surface.
         * See NNormalSurface::octs() for further details.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested octagons reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param octType the type of this octagon in the given tetrahedron;
         * this should be 0, 1 or 2.
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of octagonal discs of the given type.
         */
        virtual NLargeInteger octs(size_t tetIndex,
            int octType, const NTriangulation* triang) const = 0;
        /**
         * Deprecated routine that returns the number of octagonal discs
         * of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to octs().
         * See the octs() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getOctCoord(size_t tetIndex,
            int octType, const NTriangulation* triang) const;
        /**
         * Returns the number of times this normal surface crosses the
         * given edge.
         * See NNormalSurface::edgeWeight() for further details.
         *
         * @param edgeIndex the index in the triangulation of the edge
         * in which we are interested; this should be between 0 and
         * NTriangulation::countEdges()-1 inclusive.
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of times this normal surface crosses the
         * given edge.
         */
        virtual NLargeInteger edgeWeight(size_t edgeIndex,
            const NTriangulation* triang) const = 0;
        /**
         * Deprecated routine that returns the number of times this
         * normal surfaces crosses the given edge.
         *
         * \deprecated This routine has been renamed to edgeWeight().
         * See the edgeWeight() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getEdgeWeight(size_t edgeIndex,
            const NTriangulation* triang) const;
        /**
         * Returns the number of arcs in which this normal surface
         * intersects the given triangle in the given direction.
         * See NNormalSurface::arcs() for further details.
         *
         * @param triIndex the index in the triangulation of the triangle
         * in which we are interested; this should be between 0 and
         * NTriangulation::countTriangles()-1 inclusive.
         * @param triVertex the vertex of the triangle (0, 1 or 2) around
         * which the arcs of intersection that we are interested in lie;
         * only these arcs will be counted.
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of times this normal surface intersect the
         * given triangle with the given arc type.
         */
        virtual NLargeInteger arcs(size_t triIndex,
            int triVertex, const NTriangulation* triang) const = 0;
        /**
         * Deprecated routine that returns the number of arcs in which this
         * normal surface intersects the given triangle in the given direction.
         *
         * \deprecated This routine has been renamed to arcs().
         * See the arcs() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getTriangleArcs(size_t triIndex,
            int triVertex, const NTriangulation* triang) const;
        /**
         * A deprecated alias for arcs().
         *
         * This routine returns the number of arcs in which this normal
         * surface intersects the given triangle in the given direction.
         * See arcs() for further details.
         *
         * Since this is an alias only, it is non-virtual and cannot be
         * overridden.  Its implementation simply calls arcs().
         *
         * \deprecated This routine will be removed in a future version
         * of Regina.  Please use arcs() instead.
         *
         * @param triIndex the index in the triangulation of the triangle
         * in which we are interested; this should be between 0 and
         * NTriangulation::countTriangles()-1 inclusive.
         * @param triVertex the vertex of the triangle (0, 1 or 2) around
         * which the arcs of intersection that we are interested in lie;
         * only these arcs will be counted.
         * @param triang the triangulation in which this normal surface lives.
         * @return the number of times this normal surface intersect the
         * given triangle with the given arc type.
         */
        REGINA_DEPRECATED NLargeInteger getFaceArcs(size_t triIndex,
            int triVertex, const NTriangulation* triang) const;

        /**
         * Returns a new normal surface vector of the appropriate length
         * for the given triangulation and for the coordinate
         * system corresponding to this subclass of NNormalSurfaceVector.
         * All elements of the new vector will be initialised to zero.
         *
         * See regina::makeZeroVector() for further details.
         *
         * @param triangulation the triangulation upon which the
         * underlying coordinate system is based.
         * @return a new zero vector of the correct class and length.
         */
        #ifdef __DOXYGEN
            static NNormalSurfaceVector* makeZeroVector(
                const NTriangulation* triangulation);
        #endif
        /**
         * Creates a new set of normal surface matching equations for
         * the given triangulation using the coordinate
         * system corresponding to this particular subclass of
         * NNormalSurfaceVector.
         *
         * See regina::makeMatchingEquations() for further details.
         *
         * @param triangulation the triangulation upon which these
         * matching equations will be based.
         * @return a newly allocated set of matching equations.
         */
        #ifdef __DOXYGEN
            static NMatrixInt* makeMatchingEquations(
                const NTriangulation* triangulation);
        #endif
        /**
         * Creates a new set of validity constraints representing
         * the condition that normal surfaces be embedded.  The
         * validity constraints will be expressed relative to the
         * coordinate system corresponding to this particular
         * subclass of NNormalSurfaceVector.
         *
         * @param triangulation the triangulation upon which these
         * validity constraints will be based.
         * @return a newly allocated set of constraints.
         */
        #ifdef __DOXYGEN
            static NEnumConstraintList* makeEmbeddedConstraints(
                const NTriangulation* triangulation);
        #endif
};

/**
 * Represents a single normal surface in a 3-manifold.
 * Once the underlying triangulation changes, this normal surface object
 * is no longer valid.
 *
 * The information provided by the various query methods is independent
 * of the underlying coordinate system being used.
 * See the NNormalSurfaceVector class notes for details of what to do
 * when introducing a new coordinate system.
 *
 * Note that non-compact surfaces (surfaces with infinitely many discs,
 * such as spun-normal surfaces) are allowed; in these cases, the
 * corresponding coordinate lookup routines will return
 * NLargeInteger::infinity where appropriate.
 *
 * \todo \feature Calculation of Euler characteristic and orientability
 * for non-compact surfaces.
 * \todo \featurelong Determine which faces in the solution space a
 * normal surface belongs to.
 */
class REGINA_API NNormalSurface :
        public ShortOutput<NNormalSurface>,
        public boost::noncopyable {
    protected:
        NNormalSurfaceVector* vector;
            /**< Contains the coordinates of the normal surface in whichever
             *   space is appropriate. */
        const NTriangulation* triangulation_;
            /**< The triangulation in which this normal surface resides. */

        std::string name_;
            /**< An optional name associated with this surface. */

        mutable NProperty<NDiscType> octPosition_;
            /**< The position of the first non-zero octagonal coordinate,
                 or NDiscType::NONE if there is no non-zero octagonal
                 coordinate.  Here NDiscType::type is an octagon type
                 between 0 and 2 inclusive. */
        mutable NProperty<NLargeInteger> eulerChar_;
            /**< The Euler characteristic of this surface. */
        mutable NProperty<bool> orientable;
            /**< Is this surface orientable? */
        mutable NProperty<bool> twoSided;
            /**< Is this surface two-sided? */
        mutable NProperty<bool> connected;
            /**< Is this surface connected? */
        mutable NProperty<bool> realBoundary;
            /**< Does this surface have real boundary (i.e. does it meet
             *   any boundary triangles)? */
        mutable NProperty<bool> compact;
            /**< Is this surface compact (i.e. does it only contain
             *   finitely many discs)? */

    public:
        /**
         * Creates a new normal surface inside the given triangulation
         * with the given coordinate vector.
         *
         * This normal surface will claim ownership of the given vector
         * (i.e., you should not change or delete the vector yourself
         * afterwards).
         *
         * \pre The given coordinate vector represents a
         * normal surface inside the given triangulation.
         * \pre The given coordinate vector cannot be the null pointer.
         *
         * \ifacespython Not present.
         *
         * @param triang the triangulation in which this normal surface resides.
         * @param newVector a vector containing the coordinates of the
         * normal surface in whichever space is appropriate.
         */
        NNormalSurface(const NTriangulation* triang,
            NNormalSurfaceVector* newVector);

        /**
         * A Python-only routine that creates a new normal surface
         * inside the given triangulation with the given coordinate vector.
         *
         * \pre The given coordinate system is one in which Regina is
         * able to enumerate and store normal surfaces (not a system
         * like regina::NS_EDGE_WEIGHT, which is for viewing purposes only).
         * \pre The given coordinate vector represents a normal surface
         * inside the given triangulation (in particular, it satisfies the
         * relevant system of matching equations).  This will not be checked,
         * and things \e will go wrong if you break it.
         *
         * \ifacescpp Not available; this routine is for Python only.
         *
         * @param triang the triangulation in which this normal surface resides.
         * @param coordSystem the coordinate system used by this normal surface.
         * @param allCoords the corresponding vector of normal coordinates,
         * expressed as a Python list.  The list elements will be
         * converted internally to NLargeInteger objects.
         */
        #ifdef __DOXYGEN
        NNormalSurface(const NTriangulation* triang, NormalCoords coordSystem,
            List allCoords);
        #endif

        /**
         * Destroys this normal surface.
         * The underlying vector of coordinates will also be deallocated.
         */
        ~NNormalSurface();

        /**
         * Creates a newly allocated clone of this normal surface.
         *
         * The name of the normal surface will \e not be copied to the
         * clone; instead the clone will have an empty name.
         *
         * @return a clone of this normal surface.
         */
        NNormalSurface* clone() const;

        /**
         * Creates a newly allocated surface that is the double of this
         * surface.
         *
         * @return the double of this normal surface.
         */
        NNormalSurface* doubleSurface() const;

        /**
         * Returns the number of triangular discs of the given type in
         * this normal surface.
         * A triangular disc type is identified by specifying a
         * tetrahedron and a vertex of that tetrahedron that the
         * triangle surrounds.
         *
         * If you are using a coordinate system that adorns discs with
         * additional information (such as orientation), this routine
         * returns the \e total number of triangles in the given
         * tetrahedron of the given type.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested triangles reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param vertex the vertex of the given tetrahedron around
         * which the requested triangles lie; this should be between 0
         * and 3 inclusive.
         * @return the number of triangular discs of the given type.
         */
        NLargeInteger triangles(size_t tetIndex, int vertex) const;
        /**
         * Deprecated routine that returns the number of triangular discs
         * of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to triangles().
         * See the triangles() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getTriangleCoord(size_t tetIndex,
            int vertex) const;

        /**
         * Returns the number of oriented triangular discs of the given type 
         * in this normal surface.
         *
         * This routine is for coordinate systems that support
         * transversely oriented normal surfaces; for details see
         * "The Thurston norm via normal surfaces", Stephan Tillmann and
         * Daryl Cooper, Pacific Journal of Mathematics 239 (2009), 1-15.
         *
         * An oriented triangular disc type is identified by specifying a
         * tetrahedron, a vertex of that tetrahedron that the
         * triangle surrounds, and a boolean orientation.  The \c true
         * orientation indicates a transverse orientation pointing to the
         * nearby vertex, and the \c false orientation indicates a
         * transverse orientation pointing to the opposite face.
         *
         * If the underlying coordinate system does not support transverse
         * orientation, this routine will simply return zero.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested triangles reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param vertex the vertex of the given tetrahedron around
         * which the requested triangles lie; this should be between 0
         * and 3 inclusive.
         * @param orientation the orientation of the triangle 
         * @return the number of triangular discs of the given type.
         */
        NLargeInteger orientedTriangles(size_t tetIndex,
            int vertex, bool orientation) const;
        /**
         * Deprecated routine that returns the number of oriented
         * triangular discs of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to orientedTriangles().
         * See the orientedTriangles() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getOrientedTriangleCoord(
            size_t tetIndex, int vertex, bool orientation) const;
        /**
         * Returns the number of quadrilateral discs of the given
         * type in this normal surface.
         *
         * In each tetrahedron, there are three types of quadrilaterals,
         * defined by how they separate the four tetrahedron vertices into
         * two pairs.  Quadrilateral type \a i (for \a i = 0, 1 or 2)
         * is defined to separate edge \a i of the tetrahedron from edge
         * (5-\a i).  That is:
         *
         * - type 0 separates vertices 0,1 of the tetrahedron from vertices 2,3;
         * - type 1 separates vertices 0,2 of the tetrahedron from vertices 1,3;
         * - type 2 separates vertices 0,3 of the tetrahedron from vertices 1,2.
         *
         * If you are using a coordinate system that adorns discs with
         * additional information (such as orientation), this routine
         * returns the \e total number of quadrilaterals in the given
         * tetrahedron of the given type.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested quadrilaterals reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param quadType the type of this quadrilateral in the given
         * tetrahedron; this should be 0, 1 or 2, as described above.
         * @return the number of quadrilateral discs of the given type.
         */
        NLargeInteger quads(size_t tetIndex, int quadType) const;
        /**
         * Deprecated routine that returns the number of quadrilateral discs
         * of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to quads().
         * See the quads() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getQuadCoord(size_t tetIndex,
            int quadType) const;
        /**
         * Returns the number of oriented quadrilateral discs of the given type
         * in this normal surface.
         *
         * This routine is for coordinate systems that support
         * transversely oriented normal surfaces; for details see
         * "The Thurston norm via normal surfaces", Stephan Tillmann and
         * Daryl Cooper, Pacific Journal of Mathematics 239 (2009), 1-15.
         *
         * An oriented quadrilateral disc type is identified by specifying
         * a tetrahedron, a quadrilateral type (0, 1 or 2) as described
         * in quads(), and a boolean orientation.
         * The \c true orientation indicates a transverse orientation
         * pointing to the edge containing vertex 0 of the tetrahedron,
         * and the \c false orientation indicates a transverse
         * orientation pointing to the opposite edge.
         *
         * If the underlying coordinate system does not support transverse
         * orientation, this routine will simply return zero.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested quadrilaterals reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param quadType the type of this quadrilateral in the given
         * tetrahedron; this should be 0, 1 or 2, as described above.
         * @param orientation the orientation of the quadrilateral disc 
         * @return the number of quadrilateral discs of the given type.
         */
        NLargeInteger orientedQuads(size_t tetIndex,
            int quadType, bool orientation) const;
        /**
         * Deprecated routine that returns the number of oriented
         * quadrilateral discs of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to orientedQuads().
         * See the orientedQuads() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getOrientedQuadCoord(size_t tetIndex,
            int quadType, bool orientation) const;
        /**
         * Returns the number of octagonal discs of the given type
         * in this normal surface.
         *
         * In each tetrahedron, there are three types of octagons,
         * defined by how they separate the four tetrahedron vertices into
         * two pairs.  Octagon type \a i (for \a i = 0, 1 or 2) is defined to
         * intersect edges \a i and (5-\a i) of the tetrahedron twice each,
         * and to intersect the remaining edges once each.  This means:
         *
         * - type 0 separates vertices 0,1 of the tetrahedron from vertices 2,3;
         * - type 1 separates vertices 0,2 of the tetrahedron from vertices 1,3;
         * - type 2 separates vertices 0,3 of the tetrahedron from vertices 1,2.
         *
         * If you are using a coordinate system that adorns discs with
         * additional information (such as orientation), this routine
         * returns the \e total number of octagons in the given
         * tetrahedron of the given type.
         *
         * @param tetIndex the index in the triangulation of the
         * tetrahedron in which the requested octagons reside;
         * this should be between 0 and
         * NTriangulation::size()-1 inclusive.
         * @param octType the type of this octagon in the given tetrahedron;
         * this should be 0, 1 or 2, as described above.
         * @return the number of octagonal discs of the given type.
         */
        NLargeInteger octs(size_t tetIndex, int octType) const;
        /**
         * Deprecated routine that returns the number of octagonal discs
         * of the given type in this normal surface.
         *
         * \deprecated This routine has been renamed to octs().
         * See the octs() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getOctCoord(size_t tetIndex,
            int octType) const;
        /**
         * Returns the number of times this normal surface crosses the
         * given edge.
         *
         * @param edgeIndex the index in the triangulation of the edge
         * in which we are interested; this should be between 0 and
         * NTriangulation::countEdges()-1 inclusive.
         * @return the number of times this normal surface crosses the
         * given edge.
         */
        NLargeInteger edgeWeight(size_t edgeIndex) const;
        /**
         * Deprecated routine that returns the number of times this
         * normal surfaces crosses the given edge.
         *
         * \deprecated This routine has been renamed to edgeWeight().
         * See the edgeWeight() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getEdgeWeight(size_t edgeIndex) const;
        /**
         * Returns the number of arcs in which this normal surface
         * intersects the given triangle in the given direction.
         *
         * @param triIndex the index in the triangulation of the triangle
         * in which we are interested; this should be between 0 and
         * NTriangulation::countTriangles()-1 inclusive.
         * @param triVertex the vertex of the triangle (0, 1 or 2) around
         * which the arcs of intersection that we are interested in lie;
         * only these arcs will be counted.
         * @return the number of times this normal surface intersect the
         * given triangle with the given arc type.
         */
        NLargeInteger arcs(size_t triIndex, int triVertex) const;
        /**
         * Deprecated routine that returns the number of arcs in which this
         * normal surface intersects the given triangle in the given direction.
         *
         * \deprecated This routine has been renamed to arcs().
         * See the arcs() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getTriangleArcs(size_t triIndex,
            int triVertex) const;
        /**
         * A deprecated alias for arcs().
         *
         * This routine returns the number of arcs in which this normal
         * surface intersects the given triangle in the given direction.
         * See arcs() for further details.
         *
         * \deprecated This routine will be removed in a future version
         * of Regina.  Please use arcs() instead.
         *
         * @param triIndex the index in the triangulation of the triangle
         * in which we are interested; this should be between 0 and
         * NTriangulation::countTriangles()-1 inclusive.
         * @param triVertex the vertex of the triangle (0, 1 or 2) around
         * which the arcs of intersection that we are interested in lie;
         * only these arcs will be counted.
         * @return the number of times this normal surface intersect the
         * given triangle with the given arc type.
         */
        REGINA_DEPRECATED NLargeInteger getFaceArcs(size_t triIndex,
            int triVertex) const;

        /**
         * Determines the first coordinate position at which this surface
         * has a non-zero octagonal coordinate.  In other words, if this
         * routine returns the disc type \a t, then the octagonal
         * coordinate returned by octs(t.tetIndex, t.type) is non-zero.
         * Here NDiscType::type represents an octagon type within a
         * tetrahedron, and takes values between 0 and 2 inclusive.
         *
         * If this surface does not contain any octagons, this routine
         * returns NDiscType::NONE instead.
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.  Moreover, if the underlying coordinate
         * system does not support almost normal surfaces, then even the
         * first call is fast (it returns NDiscType::NONE immediately).
         *
         * @return the position of the first non-zero octagonal coordinate,
         * or NDiscType::NONE if there is no such coordinate.
         */
        NDiscType octPosition() const;
        /**
         * Deprecated routine that determines the first coordinate position
         * at which this surface has a non-zero octagonal coordinate.
         *
         * \deprecated This routine has been renamed to octPosition().
         * See the octPosition() documentation for further details.
         */
        REGINA_DEPRECATED NDiscType getOctPosition() const;

        /**
         * Returns the number of coordinates in the specific underlying
         * coordinate system being used.
         *
         * @return the number of coordinates.
         */
        size_t countCoords() const;
        /**
         * Deprecated routine that returns the number of coordinates in the
         * specific underlying coordinate system being used.
         *
         * \deprecated This routine has been renamed to countCoords().
         * See the countCoords() documentation for further details.
         */
        REGINA_DEPRECATED size_t getNumberOfCoords() const;
        /**
         * Returns the triangulation in which this normal surface resides.
         *
         * @return the underlying triangulation.
         */
        const NTriangulation* triangulation() const;
        /**
         * Deprecated routine that returns the triangulation in which this
         * normal surface resides.
         *
         * \deprecated This routine has been renamed to triangulation().
         * See the triangulation() documentation for further details.
         */
        REGINA_DEPRECATED const NTriangulation* getTriangulation() const;

        /**
         * Returns the name associated with this normal surface.
         * Names are optional and need not be unique.
         * The default name for a surface is the empty string.
         *
         * @return the name of associated with this surface.
         */
        const std::string& name() const;
        /**
         * Deprecated routine that returns the name associated with this
         * normal surface.
         *
         * \deprecated This routine has been renamed to name().
         * See the name() documentation for further details.
         */
        REGINA_DEPRECATED const std::string& getName() const;
        /**
         * Sets the name associated with this normal surface.
         * Names are optional and need not be unique.
         * The default name for a surface is the empty string.
         *
         * @param newName the new name to associate with this surface.
         */
        void setName(const std::string& newName);

        /**
         * Writes this surface to the given output stream, using
         * standard triangle-quad-oct coordinates.  Octagonal coordinates
         * will only be written if the surface is stored using a coordinate
         * system that supports almost normal surfaces.
         *
         * \ifacespython Not present.
         *
         * @param out the output stream to which to write.
         */
        void writeTextShort(std::ostream& out) const;
        /**
         * Writes the underlying coordinate vector to the given output
         * stream in text format.
         * No indication will be given as to which coordinate
         * system is being used or what each coordinate means.
         * No newline will be written.
         *
         * \ifacespython The paramater \a out does not exist, and is
         * taken to be standard output.
         *
         * @param out the output stream to which to write.
         */
        void writeRawVector(std::ostream& out) const;

        /**
         * Writes a chunk of XML containing this normal surface and all
         * of its properties.  This routine will be called from within
         * NNormalSurfaceList::writeXMLPacketData().
         *
         * \ifacespython Not present.
         *
         * @param out the output stream to which the XML should be written.
         */
        void writeXMLData(std::ostream& out) const;

        /**
         * Determines if this normal surface is empty (has no discs
         * whatsoever).
         */
        bool isEmpty() const;
        /**
         * Determines if this normal surface is compact (has
         * finitely many discs).
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * @return \c true if and only if this normal surface is compact.
         */
        bool isCompact() const;
        /**
         * Returns the Euler characteristic of this surface.
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * \pre This normal surface is compact (has finitely many discs).
         *
         * @return the Euler characteristic.
         */
        NLargeInteger eulerChar() const;
        /**
         * Deprecated routine that returns the Euler characteristic of this
         * surface.
         *
         * \deprecated This routine has been renamed to eulerChar().
         * See the eulerChar() documentation for further details.
         */
        REGINA_DEPRECATED NLargeInteger getEulerChar() const;
        /**
         * A deprecated alias for eulerChar().
         *
         * Returns the Euler characteristic of this surface.
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * \pre This normal surface is compact (has finitely many discs).
         *
         * \deprecated This routine will be removed in a future version of
         * Regina.  Please use the identical routine eulerChar() instead.
         *
         * @return the Euler characteristic.
         */
        REGINA_DEPRECATED NLargeInteger getEulerCharacteristic() const;
        /**
         * Returns whether or not this surface is orientable.
         * 
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * \pre This normal surface is compact (has finitely many discs).
         *
         * \warning This routine explicitly builds the normal discs,
         * and so may run out of memory if the normal coordinates
         * are extremely large.
         *
         * @return \c true if this surface is orientable, or \c false if
         * this surface is non-orientable.
         */
        bool isOrientable() const;
        /**
         * Returns whether or not this surface is two-sided.
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * \pre This normal surface is compact (has finitely many discs).
         *
         * \warning This routine explicitly builds the normal discs,
         * and so may run out of memory if the normal coordinates
         * are extremely large.
         *
         * @return \c true if this surface is two-sided, or \c false if
         * this surface is one-sided.
         */
        bool isTwoSided() const;
        /**
         * Returns whether or not this surface is connected.
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * \pre This normal surface is compact (has finitely many discs).
         *
         * \warning This routine explicitly builds the normal discs,
         * and so may run out of memory if the normal coordinates
         * are extremely large.
         *
         * @return \c true if this surface is connected, or \c false if
         * this surface is disconnected.
         */
        bool isConnected() const;
        /**
         * Determines if this surface has any real boundary, that is,
         * whether it meets any boundary triangles of the triangulation.
         *
         * This routine caches its results, which means that once it has
         * been called for a particular surface, subsequent calls return
         * the answer immediately.
         *
         * @return \c true if and only if this surface has real boundary.
         */
        bool hasRealBoundary() const;

        /**
         * Determines whether or not this surface is vertex linking.
         * A <i>vertex linking</i> surface contains only triangles.
         *
         * Note that the results of this routine are not cached.
         * Thus the results will be reevaluated every time this routine is
         * called.
         *
         * \todo \opt Cache results.
         *
         * @return \c true if and only if this surface is vertex linking.
         */
        bool isVertexLinking() const;
        /**
         * Determines whether or not a rational multiple of this surface
         * is the link of a single vertex.
         *
         * Note that the results of this routine are not cached.
         * Thus the results will be reevaluated every time this routine is
         * called.
         *
         * \todo \opt Cache results.
         *
         * @return the vertex linked by this surface, or 0 if this
         * surface is not the link of a single vertex.
         */
        const NVertex* isVertexLink() const;
        /**
         * Determines whether or not a rational multiple of this surface
         * is the thin link of a single edge.
         *
         * If there are two different edges <i>e1</i> and <i>e2</i> for
         * which this surface could be expressed as the thin link of
         * either <i>e1</i> or <i>e2</i>, the pair
         * (<i>e1</i>,<i>e2</i>) will be returned.
         * If this surface is the thin link of only one edge <i>e</i>,
         * the pair (<i>e</i>,0) will be returned.
         * If this surface is not the thin link of any edges, the pair
         * (0,0) will be returned.
         *
         * Note that the results of this routine are not cached.
         * Thus the results will be reevaluated every time this routine is
         * called.
         *
         * \todo \opt Cache results.
         *
         * \ifacespython This routine returns a tuple of size 2.
         *
         * @return a pair containing the edge(s) linked by this surface,
         * as described above.
         */
        std::pair<const NEdge*, const NEdge*> isThinEdgeLink() const;
        /**
         * Determines whether or not this surface is a splitting surface.
         * A \a splitting surface is a compact surface containing
         * precisely one quad per tetrahedron and no other normal (or
         * almost normal) discs.
         *
         * Note that the results of this routine are not cached.
         * Thus the results will be reevaluated every time this routine is
         * called.
         *
         * \todo \opt Cache results.
         *
         * @return \c true if and only if this is a splitting surface.
         */
        bool isSplitting() const;
        /**
         * Determines whether or not this surface is a central surface.
         * A \a central surface is a compact surface containing
         * at most one normal or almost normal disc per tetrahedron.
         * If this surface is central, the number of tetrahedra that it meets
         * (i.e., the number of discs in the surface) will be returned.
         *
         * Note that the results of this routine are not cached.
         * Thus the results will be reevaluated every time this routine is
         * called.
         *
         * \todo \opt Cache results.
         *
         * @return the number of tetrahedra that this surface meets if it
         * is a central surface, or 0 if it is not a central surface.
         */
        NLargeInteger isCentral() const;

        /**
         * Determines whether this surface represents a compressing disc
         * in the underlying 3-manifold.
         *
         * Let this surface be \a D and let the underlying 3-manifold
         * be \a M with boundary \a B.  To be a compressing disc, \a D must
         * be a properly embedded disc in \a M, and the boundary of \a D
         * must not bound a disc in \a B.
         *
         * The implementation of this routine is somewhat inefficient at
         * present, since it cuts along the disc, retriangulates and then
         * examines the resulting boundary components.
         *
         * \pre This normal surface is compact and embedded.
         * \pre This normal surface contains no octagonal discs.
         *
         * \todo \opt Reimplement this to avoid cutting along surfaces.
         * \todo \prob Check for absurdly large numbers of discs and bail
         * accordingly.
         *
         * \warning This routine might cut along the surface and
         * retriangulate, and so may run out of memory if the normal
         * coordinates are extremely large.
         *
         * @param knownConnected \c true if this normal surface is
         * already known to be connected (for instance, if it came from
         * an enumeration of vertex normal surfaces), or \c false if
         * we should not assume any such information about this surface.
         * @return \c true if this surface is a compressing disc, or \c false if
         * this surface is not a compressing disc.
         */
        bool isCompressingDisc(bool knownConnected = false) const;

        /**
         * Determines whether this is an incompressible surface within
         * the surrounding 3-manifold.  At present, this routine is only
         * implemented for surfaces embedded within \e closed and
         * \e irreducible 3-manifold triangulations.
         *
         * Let \a D be some disc embedded in the underlying 3-manifold,
         * and let \a B be the boundary of \a D.  We call \a D a
         * <i>compressing disc</i> for this surface if (i) the intersection
         * of \a D with this surface is the boundary \a B, and
         * (ii) although \a B bounds a disc within the 3-manifold, it
         * does not bound a disc within this surface.
         *
         * We declare this surface to be \e incompressible if there are
         * no such compressing discs.  For our purposes, spheres are never
         * considered incompressible (so if this surface is a sphere then
         * this routine will always return \c false).
         *
         * This test is designed exclusively for two-sided surfaces.
         * If this surface is one-sided, the incompressibility test will
         * be run on its two-sided double cover.
         *
         * \warning This routine may in some circumstances be extremely slow.
         * This is because the underlying algorithm cuts along this surface,
         * retriangulates (possibly using a very large number of tetrahedra),
         * and then searches for a normal compressing disc in each
         * component of the cut-open triangulation.
         *
         * \pre The underlying triangulation is valid and closed, and
         * represents an irreducible 3-manifold.
         * \pre This normal surface is compact, embedded and connected,
         * and contains no octagonal discs.
         *
         * @return \c true if this surface is incompressible, or \c false if
         * this surface is not incompressible (or if it is a sphere).
         */
        bool isIncompressible() const;

        /**
         * Cuts the associated triangulation along this surface and
         * returns a newly created resulting triangulation.
         * The original triangulation is not changed.
         *
         * Note that, unlike crushing a surface to a point, this
         * operation will not change the topology of the underlying
         * 3-manifold beyond simply slicing along this surface.
         *
         * \warning The number of tetrahedra in the new triangulation
         * can be <i>very</i> large.
         *
         * \pre This normal surface is compact and embedded.
         * \pre This normal surface contains no octagonal discs.
         *
         * @return a pointer to the newly allocated resulting
         * triangulation.
         */
        NTriangulation* cutAlong() const;

        /**
         * Crushes this surface to a point in the associated
         * triangulation and returns a newly created resulting
         * triangulation.  The original triangulation is not changed.
         *
         * Crushing the surface will produce a number of tetrahedra,
         * triangular pillows and/or footballs.  The pillows and
         * footballs will then be flattened to triangles and edges
         * respectively (resulting in the possible
         * changes mentioned below) to produce a proper triangulation.
         *
         * Note that the new triangulation will have at most the same
         * number of tetrahedra as the old triangulation, and will have
         * strictly fewer tetrahedra if this surface is not vertex
         * linking.
         *
         * The act of flattening pillows and footballs as described
         * above can lead to unintended topological side-effects, beyond
         * the effects of merely cutting along this surface and
         * identifying the new boundary surface(s) to points.
         * Examples of these unintended side-effects can include
         * connected sum decompositions, removal of 3-spheres and
         * small Lens spaces and so on; a full list of possible changes
         * is beyond the scope of this API documentation.
         *
         * \warning This routine can have unintended topological
         * side-effects, as described above.
         * \warning In exceptional cases with non-orientable
         * 3-manifolds, these side-effects might lead to invalid edges
         * (edges whose midpoints are projective plane cusps).
         *
         * \pre This normal surface is compact and embedded.
         * \pre This normal surface contains no octagonal discs.
         *
         * @return a pointer to the newly allocated resulting
         * triangulation.
         */
        NTriangulation* crush() const;

        /**
         * Determines whether this and the given surface in fact
         * represent the same normal (or almost normal) surface.
         *
         * Specifically, this routine examines (or computes) the number of
         * normal or almost normal discs of each type, and returns \c true
         * if and only if these counts are the same for both surfaces.
         *
         * It does not matter what coordinate systems the two surfaces
         * use.  In particular, it does not matter if this and the
         * given surface use different coordinate systems, and it
         * does not matter if one surface uses an almost normal
         * coordinate system and the other does not.
         *
         * \pre Both this and the given normal surface live within the
         * same 3-manifold triangulation.
         *
         * @param other the surface to be compared with this surface.
         * @return \c true if both surfaces represent the same normal or
         * almost normal surface, or \c false if not.
         */
        bool sameSurface(const NNormalSurface& other) const;

        /**
         * Determines whether this surface contains only triangle and/or
         * quadrilateral discs.  This is to distinguish normal surfaces
         * from more general surfaces such as almost normal surfaces
         * (which also contain octagonal pieces).
         *
         * Even if the underlying coordinate system supports other
         * disc types (such as octagons), this routine will still return
         * \c true if this particular surface does not use them.
         * This is in contrast to the routine
         * NNormalSurfaceList::allowsAlmostNormal(), which only examines
         * the underlying coordinate system.
         *
         * @return \c true if and only if this surface contains only
         * triangles and/or quadrilaterals.
         */
        bool normal() const;

        /**
         * Determines whether this surface is embedded.  This is true if
         * and only if the surface contains no conflicting quadrilateral
         * and/or octagon types.
         *
         * @return \c true if and only if this surface is embedded.
         */
        bool embedded() const;

        /**
         * Determines whether this and the given surface are locally compatible.
         * Local compatibility means that, within each individual tetrahedron
         * of the triangulation, it is possible to arrange the normal
         * discs of both surfaces so that none intersect.
         *
         * This is a local constraint, not a global constraint.  That is,
         * we do not insist that we can avoid intersections within all
         * tetrahedra \e simultaneously.  To test the global constraint,
         * see the (much slower) routine disjoint() instead.
         *
         * Local compatibility can be formulated in terms of normal disc types.
         * Two normal (or almost normal) surfaces are locally compatible if
         * and only if they together have at most one quadrilateral or
         * octagonal disc type per tetrahedron.
         *
         * Note again that this is a local constraint only.  In particular,
         * for almost normal surfaces, it does \e not insist that there is
         * at most one octagonal disc type anywhere within the triangulation.
         *
         * If one of the two surfaces breaks the local compatibility
         * constraints on its own (for instance, it contains two different
         * quadrilateral disc types within the same tetrahedron), then this
         * routine will return \c false regardless of what the other surface
         * contains.
         *
         * \pre Both this and the given normal surface live within the
         * same 3-manifold triangulation.
         *
         * @param other the other surface to test for local compatibility with
         * this surface.
         * @return \c true if the two surfaces are locally compatible, or
         * \c false if they are not.
         */
        bool locallyCompatible(const NNormalSurface& other) const;

        /**
         * Determines whether this and the given surface can be placed
         * within the surrounding triangulation so that they do not intersect
         * anywhere at all, without changing either normal isotopy class.
         *
         * This is a global constraint, and therefore gives a stronger test
         * than locallyCompatible().  However, this global constraint is
         * also much slower to test; the running time is proportional to
         * the total number of normal discs in both surfaces.
         *
         * Note that this routine has a number of preconditions.  Most
         * importantly, it will only work if both this and the given
         * surface use the \e same coordinate system.
         * Running this test over two surfaces with different coordinate
         * systems could give unpredictable results, and might
         * crash the program entirely.
         *
         * \pre Both this and the given normal surface live within the
         * same 3-manifold triangulation.
         * \pre Both this and the given normal surface are stored using
         * the same coordinate system (i.e., the same
         * subclass of NNormalSurfaceVector).
         * \pre Both this and the given surface are compact (have
         * finitely many discs), embedded, non-empty and connected.
         *
         * @param other the other surface to test alongside this surface
         * for potential intersections.
         * @return \c true if both surfaces can be embedded without
         * intersecting anywhere, or \c false if this and the given
         * surface are forced to intersect at some point.
         */
        bool disjoint(const NNormalSurface& other) const;

        /**
         * Computes the information about the boundary slopes of this surface
         * at each cusp of the triangulation.  This is for use with spun-normal
         * surfaces (since for closed surfaces all boundary slopes are zero).
         *
         * This routine is only available for use with SnapPea triangulations,
         * since it needs to know the specific meridian and longitude on each
         * cusp.  This information is \e only available through the SnapPea
         * kernel, since Regina does not use or store peripheral curves for
         * its own NTriangulation class.  Therefore, if the underlying
         * triangulation (as returned by triangulation()) is not of the
         * subclass NSnapPeaTriangulation, this routine will simply return 0.
         *
         * All cusps are treated as complete.  That is, any Dehn fillings
         * stored in the SnapPea triangulation will be ignored.
         *
         * The results are returned in a matrix with \a V rows and two
         * columns, where \a V is the number of vertices in the triangulation.
         * If row \a i of the matrix contains the integers
         * \a M and \a L, this indicates that at the <i>i</i>th cusp,
         * the boundary curves have algebraic intersection number \a M
         * with the meridian and \a L with the longitude.  Equivalently,
         * the boundary curves pass \a L times around the meridian and
         * <i>-M</i> times around the longitude.
         * The rational boundary slope is therefore <tt>-L/M</tt>, and
         * there are <tt>gcd(L,M)</tt> boundary curves with this slope.
         *
         * The orientations of the boundary curves of a
         * spun-normal surface are chosen so that \e if meridian and
         * longitude are a positive basis as vieved from the cusp, then
         * as one travels along an oriented boundary curve, the
         * spun-normal surface spirals into the cusp to one's right and
         * down into the manifold to one's left.
         *
         * If the triangulation contains more than one vertex, the rows
         * in the resulting matrix are ordered by cusp index (as stored by
         * SnapPea).  You can call NSnapPeaTriangulation::cuspVertex() to
         * map these to Regina's vertex indices if needed.
         *
         * At present, Regina can only compute boundary slopes if the
         * triangulation is oriented, if every vertex link in the
         * triangulation is a torus, and if the underlying coordinate system
         * is for normal surfaces (not almost normal surfaces).  If these
         * conditions are not met, this routine will return 0.
         *
         * @author William Pettersson and Stephan Tillmann
         *
         * @return a newly allocated matrix with \a number_of_vertices
         * rows and two columns as described above, or 0 if the boundary
         * slopes cannot be computed (e.g., if the underlying triangulation
         * is not of type NSnapPeaTriangulation, or if it fails to meet the
         * preconditions outlined above).
         */
        NMatrixInt* boundaryIntersections() const;

        /**
         * Gives read-only access to the raw vector that sits beneath this
         * normal surface.
         *
         * Generally users should not need this function.  However, it is
         * provided here in case the need should arise (e.g., for reasons
         * of efficiency).
         *
         * \warning An NNormalSurface does not know what underlying
         * coordinate system its raw vector uses.  Unless you already know
         * the coordinate system in advance (i.e., you created the surface
         * yourself), it is best to keep to the coordinate-system-agnostic
         * access functions such as NNormalSurfaceVector::triangles()
         * and NNormalSurfaceVector::quads().
         *
         * \ifacespython Not present.
         *
         * @return the underlying raw vector.
         */
        const NNormalSurfaceVector* rawVector() const;

        /**
         * Searches for a non-vertex-linking normal 2-sphere within the
         * given triangulation.  If a non-vertex linking normal 2-sphere
         * exists anywhere at all within the triangulation, then this routine
         * is guaranteed to find one.
         *
         * Note that the surface returned (if any) depends upon the
         * triangulation, and so must be destroyed before the triangulation
         * itself.
         *
         * \deprecated This routine will be removed in a future version
         * of Regina.  Use NTriangulation::hasNonTrivialSphereOrDisc()
         * instead.
         *
         * @param tri the triangulation in which to search.
         * @return a newly allocated non-vertex-linking normal sphere
         * within the given triangulation, or 0 if no such sphere exists.
         */
        REGINA_DEPRECATED static NNormalSurface* findNonTrivialSphere(
            NTriangulation* tri);

        /**
         * Searches the list of vertex octagonal almost normal surfaces for
         * an almost normal 2-sphere within the given triangulation.  This
         * means that tubed almost normal 2-spheres or non-vertex octagonal
         * almost normal 2-spheres will not be found.
         *
         * This search can be done either in standard almost normal
         * coordinates (with triangles, quadrilaterals and octagons), or
         * in quadrilateral-octagon coordinates.  This choice of coordinate
         * system affects how we define "vertex".  The default is to use
         * standard coordinates (where the set of vertex surfaces is larger).
         *
         * For "sufficiently nice" triangulations, if this routine fails
         * to find an almost normal 2-sphere then we can be certain that
         * the triangulation contains no almost normal 2-spheres at all.
         * In particular, this is true for closed orientable one-vertex
         * 0-efficient triangulations.  For a proof in standard coordinates,
         * see "0-efficient triangulations of 3-manifolds", William Jaco
         * and J. Hyam Rubinstein, J. Differential Geom. 65 (2003),
         * no. 1, 61--168.  For a proof in quadrilateral-octagon coordinates,
         * see "Quadrilateral-octagon coordinates for almost normal surfaces",
         * Benjamin A. Burton, Experiment. Math. 19 (2010), 285-315.
         *
         * Note that the surface that this routine returns (if any) depends
         * upon the triangulation, and so this surface must be destroyed
         * before the triangulation is destroyed.
         *
         * \warning Currently this routine can be quite slow since it
         * performs a full enumeration of vertex almost normal surfaces.
         *
         * \deprecated This routine will be removed in a future version
         * of Regina.  Use NTriangulation::hasOctagonalAlmostNormalSphere()
         * instead, which offers significant optimisations over this routine.
         *
         * @param tri the triangulation in which to search.
         * @param quadOct \c true if we should search for vertex
         * surfaces in quadrilateral-octagon coordinates, or \c false
         * (the default) if we should search for surfaces in standard
         * almost normal coordinates.
         * @return a newly allocated vertex octagonal almost normal sphere
         * within the given triangulation, or 0 if no such sphere exists.
         */
        REGINA_DEPRECATED static NNormalSurface* findVtxOctAlmostNormalSphere(
            NTriangulation* tri, bool quadOct = false);

    protected:
        /**
         * Calculates the position of the first non-zero octagon
         * coordinate and stores it as a property.
         */
        void calculateOctPosition() const;

        /**
         * Calculates the Euler characteristic of this surface and
         * stores it as a property.
         *
         * \pre This normal surface is compact (has finitely many discs).
         */
        void calculateEulerChar() const;
        /**
         * Calculates whether this surface is orientable and/or
         * two-sided and stores the results as properties.
         *
         * \pre This normal surface is compact (has finitely many discs).
         */
        void calculateOrientable() const;
        /**
         * Calculates whether this surface has any real boundary and
         * stores the result as a property.
         */
        void calculateRealBoundary() const;

    friend class regina::NXMLNormalSurfaceReader;
};

/*@}*/

// Inline functions for NNormalSurfaceVector

inline NNormalSurfaceVector::NNormalSurfaceVector(size_t length) :
        NRay(length) {
}
inline NNormalSurfaceVector::NNormalSurfaceVector(
        const NVector<NLargeInteger>& cloneMe) : NRay(cloneMe) {
}
inline NNormalSurfaceVector::~NNormalSurfaceVector() {
}
inline NLargeInteger NNormalSurfaceVector::getTriangleCoord(size_t tetIndex,
        int vertex, const NTriangulation* triang) const {
    return triangles(tetIndex, vertex, triang);
}
inline NLargeInteger NNormalSurfaceVector::getQuadCoord(size_t tetIndex,
        int quadType, const NTriangulation* triang) const {
    return quads(tetIndex, quadType, triang);
}
inline NLargeInteger NNormalSurfaceVector::getOctCoord(size_t tetIndex,
        int octType, const NTriangulation* triang) const {
    return octs(tetIndex, octType, triang);
}
inline NLargeInteger NNormalSurfaceVector::getEdgeWeight(size_t edgeIndex,
        const NTriangulation* triang) const {
    return edgeWeight(edgeIndex, triang);
}
inline NLargeInteger NNormalSurfaceVector::getTriangleArcs(size_t triIndex,
            int triVertex, const NTriangulation* triang) const {
    return arcs(triIndex, triVertex, triang);
}
inline NLargeInteger NNormalSurfaceVector::getFaceArcs(size_t triIndex,
        int triVertex, const NTriangulation* triang) const {
    return arcs(triIndex, triVertex, triang);
}
inline NLargeInteger NNormalSurfaceVector::getOrientedTriangleCoord(
        size_t tetIndex, int vertex, const NTriangulation* triang,
        bool orientation) const {
    return orientedTriangles(tetIndex, vertex, triang, orientation);
}
inline NLargeInteger NNormalSurfaceVector::getOrientedQuadCoord(
        size_t tetIndex, int quadType, const NTriangulation* triang,
        bool orientation) const {
    return orientedQuads(tetIndex, quadType, triang, orientation);
}

// Inline functions for NNormalSurface

inline NNormalSurface::~NNormalSurface() {
    delete vector;
}

inline NLargeInteger NNormalSurface::triangles(size_t tetIndex,
        int vertex) const {
    return vector->triangles(tetIndex, vertex, triangulation_);
}
inline NLargeInteger NNormalSurface::getTriangleCoord(size_t tetIndex,
        int vertex) const {
    return vector->triangles(tetIndex, vertex, triangulation_);
}
inline NLargeInteger NNormalSurface::orientedTriangles(
        size_t tetIndex, int vertex, bool oriented) const {
    return vector->orientedTriangles(tetIndex, vertex, triangulation_,
        oriented);
}
inline NLargeInteger NNormalSurface::getOrientedTriangleCoord(
        size_t tetIndex, int vertex, bool oriented) const {
    return vector->orientedTriangles(tetIndex, vertex, triangulation_,
        oriented);
}
inline NLargeInteger NNormalSurface::quads(size_t tetIndex,
        int quadType) const {
    return vector->quads(tetIndex, quadType, triangulation_);
}
inline NLargeInteger NNormalSurface::getQuadCoord(size_t tetIndex,
        int quadType) const {
    return vector->quads(tetIndex, quadType, triangulation_);
}
inline NLargeInteger NNormalSurface::orientedQuads(
        size_t tetIndex, int quadType, bool oriented) const {
    return vector->orientedQuads(tetIndex, quadType, triangulation_,
        oriented);
}
inline NLargeInteger NNormalSurface::getOrientedQuadCoord(
        size_t tetIndex, int quadType, bool oriented) const {
    return vector->orientedQuads(tetIndex, quadType, triangulation_,
        oriented);
}
inline NLargeInteger NNormalSurface::octs(size_t tetIndex, int octType) const {
    return vector->octs(tetIndex, octType, triangulation_);
}
inline NLargeInteger NNormalSurface::getOctCoord(size_t tetIndex,
        int octType) const {
    return vector->octs(tetIndex, octType, triangulation_);
}
inline NLargeInteger NNormalSurface::edgeWeight(size_t edgeIndex)
        const {
    return vector->edgeWeight(edgeIndex, triangulation_);
}
inline NLargeInteger NNormalSurface::getEdgeWeight(size_t edgeIndex)
        const {
    return vector->edgeWeight(edgeIndex, triangulation_);
}
inline NLargeInteger NNormalSurface::arcs(size_t triIndex,
        int triVertex) const {
    return vector->arcs(triIndex, triVertex, triangulation_);
}
inline NLargeInteger NNormalSurface::getTriangleArcs(size_t triIndex,
        int triVertex) const {
    return vector->arcs(triIndex, triVertex, triangulation_);
}
inline NLargeInteger NNormalSurface::getFaceArcs(size_t triIndex,
        int triVertex) const {
    return vector->arcs(triIndex, triVertex, triangulation_);
}

inline NDiscType NNormalSurface::octPosition() const {
    if (! octPosition_.known())
        calculateOctPosition();
    return octPosition_.value();
}

inline NDiscType NNormalSurface::getOctPosition() const {
    return octPosition();
}

inline size_t NNormalSurface::countCoords() const {
    return vector->size();
}
inline size_t NNormalSurface::getNumberOfCoords() const {
    return vector->size();
}
inline const NTriangulation* NNormalSurface::triangulation() const {
    return triangulation_;
}
inline const NTriangulation* NNormalSurface::getTriangulation() const {
    return triangulation_;
}

inline const std::string& NNormalSurface::name() const {
    return name_;
}
inline const std::string& NNormalSurface::getName() const {
    return name_;
}
inline void NNormalSurface::setName(const std::string& newName) {
    name_ = newName;
}

inline void NNormalSurface::writeRawVector(std::ostream& out) const {
    out << *vector;
}

inline bool NNormalSurface::isCompact() const {
    if (! compact.known())
        compact = vector->isCompact(triangulation_);
    return compact.value();
}

inline NLargeInteger NNormalSurface::eulerChar() const {
    if (! eulerChar_.known())
        calculateEulerChar();
    return eulerChar_.value();
}

inline NLargeInteger NNormalSurface::getEulerChar() const {
    return eulerChar();
}

inline NLargeInteger NNormalSurface::getEulerCharacteristic() const {
    return eulerChar();
}

inline bool NNormalSurface::isOrientable() const {
    if (! orientable.known())
        calculateOrientable();
    return orientable.value();
}

inline bool NNormalSurface::isTwoSided() const {
    if (! twoSided.known())
        calculateOrientable();
    return twoSided.value();
}

inline bool NNormalSurface::isConnected() const {
    if (! connected.known())
        calculateOrientable();
    return connected.value();
}

inline bool NNormalSurface::hasRealBoundary() const {
    if (! realBoundary.known())
        calculateRealBoundary();
    return realBoundary.value();
}

inline bool NNormalSurface::isVertexLinking() const {
    return vector->isVertexLinking(triangulation_);
}

inline const NVertex* NNormalSurface::isVertexLink() const {
    return vector->isVertexLink(triangulation_);
}

inline std::pair<const NEdge*, const NEdge*> NNormalSurface::isThinEdgeLink()
        const {
    return vector->isThinEdgeLink(triangulation_);
}

inline bool NNormalSurface::isSplitting() const {
    return vector->isSplitting(triangulation_);
}

inline NLargeInteger NNormalSurface::isCentral() const {
    return vector->isCentral(triangulation_);
}

inline bool NNormalSurface::normal() const {
    return (octPosition() == NDiscType::NONE);
}

inline const NNormalSurfaceVector* NNormalSurface::rawVector() const {
    return vector;
}

} // namespace regina

#endif

