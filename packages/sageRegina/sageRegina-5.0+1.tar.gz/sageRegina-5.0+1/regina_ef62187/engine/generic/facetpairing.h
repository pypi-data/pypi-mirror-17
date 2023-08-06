
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

#ifndef __FACETPAIRING_H
#ifndef __DOXYGEN
#define __FACETPAIRING_H
#endif

/*! \file generic/facetpairing.h
 *  \brief Deals with dual graphs of <i>n</i>-dimensional triangulations.
 */

#include "generic/detail/facetpairing.h"

namespace regina {

/**
 * \weakgroup generic
 * @{
 */

/**
 * Represents the dual graph of a <i>dim</i>-manifold triangulation;
 * that is, the pairwise matching of facets of <i>dim</i>-dimensional simplices.
 *
 * Given a fixed number of <i>dim</i>-dimensional simplices,
 * each facet of each simplex is either paired with some other simplex facet
 * (which is in turn paired with it) or remains unmatched.
 * A simplex facet cannot be paired with itself.
 *
 * Such a matching models part of the structure of a <i>dim</i>-manifold
 * triangulation, in which each simplex facet is either glued to some
 * other simplex facet (which is in turn glued to it) or is an unglued
 * boundary facet.
 *
 * Note that if this pairing is used to construct an actual
 * triangulation, the individual gluing permutations will still need to
 * be specified; they are not a part of this structure.
 *
 * For Regina's \ref stddim "standard dimensions", this template is specialised
 * and offers more functionality.  In order to use these specialised classes,
 * you will need to include the corresponding headers (e.g.,
 * dim2/dim2edgepairing.h for \a dim = 2, or triangulation/nfacepairing.h for
 * \a dim = 3).  For convenience, there are typedefs available for these
 * specialised classes (such as Dim2EdgePairing and NFacePairing respectively).
 *
 * \ifacespython Python does not support templates.  Instead
 * this class can be used by appending the dimension as a suffix
 * (e.g., FacetPairing2 and FacetPairing3 for dimensions 2 and 3).
 * The typedefs mentioned above for standard dimensions
 * (e.g., Dim2EdgePairing and NFacePairing) are also available.
 *
 * \tparam dim the dimension of the underlying triangulation.
 * This must be between 2 and 15 inclusive.
 */
template <int dim>
class FacetPairing : public detail::FacetPairingBase<dim> {
    static_assert(dim != 3,
        "The generic implementation of FacetPairing<dim> "
        "should not be used for dimension 3.");

    public:
        /**
         * Creates a new clone of the given facet pairing.
         *
         * @param cloneMe the facet pairing to clone.
         */
        FacetPairing(const FacetPairing& cloneMe);

        /**
         * Creates the dual graph of the given triangulation.
         * This is the facet pairing that describes how the facets of
         * simplices in the given triangulation are joined together, as
         * described in the class notes.
         *
         * \pre The given triangulation is not empty.
         *
         * @param tri the triangulation whose facet pairing should
         * be constructed.
         */
        FacetPairing(const Triangulation<dim>& tri);

    private:
        /**
         * Creates a new facet pairing.
         * All internal arrays will be allocated but not initialised.
         *
         * \pre \a size is at least 1.
         *
         * @param size the number of top-dimensional simplicies under
         * consideration in this new facet pairing.
         */
        FacetPairing(size_t size);

    // Make sure the parent class can call the private constructor.
    friend class detail::FacetPairingBase<dim>;
};

// Note that some of our facet pairing classes are specialised elsewhere.
// Do not explicitly drag in the specialised headers for now.
template <> class FacetPairing<3>;

/*@}*/

// Inline functions for FacetPairing

template <int dim>
inline FacetPairing<dim>::FacetPairing(const FacetPairing& cloneMe) :
        detail::FacetPairingBase<dim>(cloneMe) {
}

template <int dim>
inline FacetPairing<dim>::FacetPairing(const Triangulation<dim>& tri) :
        detail::FacetPairingBase<dim>(tri) {
}

template <int dim>
inline FacetPairing<dim>::FacetPairing(size_t size) :
        detail::FacetPairingBase<dim>(size) {
}

} // namespace regina

#endif

