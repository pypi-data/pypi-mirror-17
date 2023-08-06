
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

/*! \file algebra/nxmlalgebrareader.h
 *  \brief Deals with parsing XML data for various algebraic structures.
 */

#ifndef __NXMLALGEBRAREADER_H
#ifndef __DOXYGEN
#define __NXMLALGEBRAREADER_H
#endif

#include "regina-core.h"
#include "algebra/nabeliangroup.h"
#include "algebra/ngrouppresentation.h"
#include "utilities/nxmlelementreader.h"

namespace regina {

/**
 * \weakgroup algebra
 * @{
 */

/**
 * An XML element reader that reads a single abelian group.
 * An abelian group is generally contained within an
 * <tt>\<abeliangroup\></tt> ... <tt>\</abeliangroup\></tt> pair.
 *
 * \ifacespython Not present.
 */
class REGINA_API NXMLAbelianGroupReader : public NXMLElementReader {
    private:
        NAbelianGroup* group_;
            /**< The abelian group currently being read. */

    public:
        /**
         * Creates a new abelian group reader.
         */
        NXMLAbelianGroupReader();

        /**
         * Returns the newly allocated abelian group that has been read by
         * this element reader.
         *
         * @return the group that has been read, or 0 if an error occurred.
         */
        virtual NAbelianGroup* group();
        /**
         * Deprecated routine that returns the newly allocated abelian group
         * that has been read by this element reader.
         *
         * \deprecated This routine has been renamed to group().
         * See the group() documentation for further details.
         */
        REGINA_DEPRECATED virtual NAbelianGroup* getGroup();

        virtual void startElement(const std::string& tagName,
            const regina::xml::XMLPropertyDict& tagProps,
            NXMLElementReader* parentReader);
        virtual void initialChars(const std::string& chars);
};

/**
 * An XML element reader that reads a single group presentation.
 * A group presentation is generally contained within a
 * <tt>\<group\></tt> ... <tt>\</group\></tt> pair.
 *
 * \ifacespython Not present.
 */
class REGINA_API NXMLGroupPresentationReader : public NXMLElementReader {
    private:
        NGroupPresentation* group_;
            /**< The group presentation currently being read. */

    public:
        /**
         * Creates a new group presentation reader.
         */
        NXMLGroupPresentationReader();

        /**
         * Returns the newly allocated group presentation that has been read by
         * this element reader.
         *
         * @return the group that has been read, or 0 if an error occurred.
         */
        virtual NGroupPresentation* group();
        /**
         * Deprecated routine that returns the newly allocated group
         * presentation that has been read by this element reader.
         *
         * \deprecated This routine has been renamed to group().
         * See the group() documentation for further details.
         */
        REGINA_DEPRECATED virtual NGroupPresentation* getGroup();

        virtual void startElement(const std::string& tagName,
            const regina::xml::XMLPropertyDict& tagProps,
            NXMLElementReader* parentReader);
        virtual NXMLElementReader* startSubElement(
            const std::string& subTagName,
            const regina::xml::XMLPropertyDict& subTagProps);
        virtual void endSubElement(const std::string& subTagName,
            NXMLElementReader* subReader);
};

/*@}*/

// Inline functions for NXMLAbelianGroupReader

inline NXMLAbelianGroupReader::NXMLAbelianGroupReader() : group_(0) {
}

inline NAbelianGroup* NXMLAbelianGroupReader::group() {
    return group_;
}

inline NAbelianGroup* NXMLAbelianGroupReader::getGroup() {
    return group_;
}

// Inline functions for NXMLGroupPresentationReader

inline NXMLGroupPresentationReader::NXMLGroupPresentationReader() : group_(0) {
}

inline NGroupPresentation* NXMLGroupPresentationReader::group() {
    return group_;
}

inline NGroupPresentation* NXMLGroupPresentationReader::getGroup() {
    return group_;
}

} // namespace regina

#endif

