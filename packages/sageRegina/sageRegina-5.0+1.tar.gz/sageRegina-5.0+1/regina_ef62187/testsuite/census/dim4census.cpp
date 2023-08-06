
/**************************************************************************
 *                                                                        *
 *  Regina - A Normal Surface Theory Calculator                           *
 *  Test Suite                                                            *
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
#include <cppunit/extensions/HelperMacros.h>
#include "census/dim4gluingpermsearcher.h"
#include "dim4/dim4triangulation.h"
#include "packet/ncontainer.h"
#include "testsuite/census/testcensus.h"

using regina::Dim4FacetPairing;
using regina::Dim4GluingPermSearcher;
using regina::Dim4Triangulation;
using regina::NBoolSet;

class Dim4CensusTest : public CppUnit::TestFixture {
    CPPUNIT_TEST_SUITE(Dim4CensusTest);

    CPPUNIT_TEST(rawCounts);
    CPPUNIT_TEST(rawCountsCompact);
    CPPUNIT_TEST(rawCountsBounded);

    CPPUNIT_TEST_SUITE_END();

    public:
        void setUp() {
        }

        void tearDown() {
        }

        void rawCounts() {
            unsigned nAll[] = { 1, 0, 23, 0, 8656, 0 };
            rawCountsCompare(1, 3, nAll, "closed/ideal",
                NBoolSet::sBoth, NBoolSet::sBoth, NBoolSet::sFalse, 0);

            unsigned nOrientable[] = { 1, 0, 15, 0, 4150, 0 };
            rawCountsCompare(1, 3, nOrientable, "closed/ideal",
                NBoolSet::sBoth, NBoolSet::sTrue, NBoolSet::sFalse, 0);
        }

        void rawCountsCompact() {
            unsigned nAll[] = { 1, 0, 10, 0 };
            rawCountsCompare(1, 3, nAll, "closed compact",
                NBoolSet::sTrue, NBoolSet::sBoth, NBoolSet::sFalse, 0);

            unsigned nOrientable[] = { 1, 0, 8, 0 };
            rawCountsCompare(1, 3, nOrientable, "closed compact orbl",
                NBoolSet::sTrue, NBoolSet::sTrue, NBoolSet::sFalse, 0);
        }

        void rawCountsBounded() {
            unsigned nAll[] = { 1, 7, 51, 939, 25265 };
            rawCountsCompare(1, 2, nAll, "bounded",
                NBoolSet::sBoth, NBoolSet::sBoth, NBoolSet::sTrue, -1);

            unsigned nCompact[] = { 1, 5, 38, 782 };
            rawCountsCompare(1, 2, nCompact, "bounded compact",
                NBoolSet::sTrue, NBoolSet::sBoth, NBoolSet::sTrue, -1);

            unsigned nOrientable[] = { 1, 4, 27, 457 };
            rawCountsCompare(1, 2, nOrientable, "bounded compact orbl",
                NBoolSet::sTrue, NBoolSet::sTrue, NBoolSet::sTrue, -1);
        }

        struct CensusSpec {
            NBoolSet finite_;
            NBoolSet orbl_;

            unsigned long count_;

            CensusSpec(NBoolSet finite, NBoolSet orbl) :
                finite_(finite), orbl_(orbl), count_(0) {}
        };

        static void foundPerms(const Dim4GluingPermSearcher* perms,
                void* spec) {
            if (perms) {
                CensusSpec* s = static_cast<CensusSpec*>(spec);
                Dim4Triangulation* tri = perms->triangulate();
                if (tri->isValid() &&
                        (! (s->orbl_ == NBoolSet::sTrue &&
                            ! tri->isOrientable())) &&
                        (! (s->orbl_ == NBoolSet::sFalse &&
                            tri->isOrientable())) &&
                        (! (s->finite_ == NBoolSet::sTrue &&
                            tri->isIdeal())) &&
                        (! (s->finite_ == NBoolSet::sFalse &&
                            ! tri->isIdeal())))
                    ++s->count_;
                delete tri;
            }
        }

        static void foundPairing(const Dim4FacetPairing* pairing,
                const Dim4FacetPairing::IsoList* autos, void* spec) {
            if (pairing) {
                CensusSpec* s = static_cast<CensusSpec*>(spec);
                Dim4GluingPermSearcher::findAllPerms(pairing, autos,
                    ! s->orbl_.hasFalse(), ! s->finite_.hasFalse(),
                    foundPerms, spec);
            }
        }

        static void rawCountsCompare(unsigned minPent, unsigned maxPent,
                const unsigned* realAns, const char* censusType,
                NBoolSet finiteness, NBoolSet orientability,
                NBoolSet boundary, int nBdryFacets) {
            for (unsigned nPent = minPent; nPent <= maxPent; nPent++) {
                CensusSpec spec(finiteness, orientability);

                Dim4FacetPairing::findAllPairings(nPent, boundary, nBdryFacets,
                    foundPairing, &spec);

                std::ostringstream msg;
                msg << "Census count for " << nPent << " pentachora ("
                    << censusType << ") should be " << realAns[nPent]
                    << ", not " << spec.count_ << '.';

                CPPUNIT_ASSERT_MESSAGE(msg.str(),
                    spec.count_ == realAns[nPent]);
            }
        }
};

void addDim4Census(CppUnit::TextUi::TestRunner& runner) {
    runner.addTest(Dim4CensusTest::suite());
}

