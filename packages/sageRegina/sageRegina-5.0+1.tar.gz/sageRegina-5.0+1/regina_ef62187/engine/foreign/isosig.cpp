
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

#include <fstream>
#include <sstream>

#include "dim2/dim2triangulation.h"
#include "dim4/dim4triangulation.h"
#include "foreign/isosig.h"
#include "packet/ncontainer.h"
#include "packet/ntext.h"
#include "triangulation/ntriangulation.h"

namespace regina {

NContainer* readIsoSigList(const char *filename, unsigned dimension,
        unsigned colSigs, int colLabels, unsigned long ignoreLines) {
    // Open the file.
    std::ifstream in(filename);
    if (! in)
        return 0;

    // Ignore the specified number of lines.
    std::string line;

    unsigned long i;
    for (i = 0; i < ignoreLines; i++) {
        std::getline(in, line);
        if (in.eof())
            return new NContainer();
    }

    // Read in and process the remaining lines.
    NContainer* ans = new NContainer();
    std::string errStrings;

    int col;
    std::string token;

    std::string isoSig;
    std::string label;
    Dim2Triangulation* tri2;
    NTriangulation* tri3;
    Dim4Triangulation* tri4;

    while(! in.eof()) {
        // Read in the next line.
        line.clear();
        std::getline(in, line);

        if (line.empty())
            continue;

        // Find the appropriate tokens.
        std::istringstream tokens(line);

        isoSig.clear();
        label.clear();
        for (col = 0; col <= static_cast<int>(colSigs) ||
                col <= colLabels; col++) {
            tokens >> token;
            if (token.empty())
                break;
            if (col == static_cast<int>(colSigs))
                isoSig = token;
            if (col == colLabels)
                label = token;
        }

        if (! isoSig.empty()) {
            // Process this isomorphism signature.
            if (dimension == 2) {
                if ((tri2 = Dim2Triangulation::fromIsoSig(isoSig))) {
                    tri2->setLabel(label.empty() ? isoSig : label);
                    ans->insertChildLast(tri2);
                } else
                    errStrings = errStrings + '\n' + isoSig;
            } else if (dimension == 3) {
                if ((tri3 = NTriangulation::fromIsoSig(isoSig))) {
                    tri3->setLabel(label.empty() ? isoSig : label);
                    ans->insertChildLast(tri3);
                } else
                    errStrings = errStrings + '\n' + isoSig;
            } else if (dimension == 4) {
                if ((tri4 = Dim4Triangulation::fromIsoSig(isoSig))) {
                    tri4->setLabel(label.empty() ? isoSig : label);
                    ans->insertChildLast(tri4);
                } else
                    errStrings = errStrings + '\n' + isoSig;
            } else
                errStrings = errStrings + '\n' + isoSig;
        }
    }

    // Finish off.
    if (! errStrings.empty()) {
        std::ostringstream msg;
        msg << "The following isomorphism string(s) could not be interpreted "
            "as " << dimension << "-manifold triangulations:\n" << errStrings;
        NText* errPkt = new NText(msg.str());
        errPkt->setLabel("Errors");
        ans->insertChildLast(errPkt);
    }

    return ans;
}

} // namespace regina
