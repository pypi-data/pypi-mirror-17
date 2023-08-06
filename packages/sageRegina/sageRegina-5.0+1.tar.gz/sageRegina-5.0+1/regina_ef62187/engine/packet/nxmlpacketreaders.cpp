
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

#include "packet/nxmlpacketreaders.h"
#include "packet/nxmltreeresolver.h"
#include "utilities/base64.h"
#include <cctype>
#include <string>

namespace regina {

/**
 * A unique namespace containing various task-specific packet readers.
 */
namespace {
    /**
     * Reads a single script variable and its value.
     */
    class NScriptVarReader : public NXMLElementReader {
        private:
            std::string name, valueID, valueLabel;

        public:
            inline void startElement(const std::string& /* tagName */,
                    const regina::xml::XMLPropertyDict& props,
                    NXMLElementReader*) {
                name = props.lookup("name");
                valueID = props.lookup("valueid");
                valueLabel = props.lookup("value");
            }

            inline const std::string& getName() {
                return name;
            }

            inline const std::string& getValueID() {
                return valueID;
            }

            inline const std::string& getValueLabel() {
                return valueLabel;
            }
    };

    /**
     * A resolution task that, after the entire XML file has been read,
     * will bind a script variable to its corresponding packet reference.
     */
    class VariableResolutionTask : public NXMLTreeResolutionTask {
        private:
            NScript* script_;
            std::string name_;
            std::string valueID_;
                /**< An internal packet ID.  Used by Regina >= 4.95. */
            std::string valueLabel_;
                /**< A packet label.  Used by Regina <= 4.94. */

        public:
            inline VariableResolutionTask(NScript* script,
                    const std::string& name,
                    const std::string& valueID,
                    const std::string& valueLabel) :
                    script_(script), name_(name), valueID_(valueID),
                    valueLabel_(valueLabel) {
            }

            inline void resolve(const NXMLTreeResolver& resolver) {
                NPacket* resolution = 0;
                if (! valueID_.empty()) {
                    NXMLTreeResolver::IDMap::const_iterator it =
                        resolver.ids().find(valueID_);
                    resolution = (it == resolver.ids().end() ? 0 : it->second);
                }
                if ((! resolution) && (! valueLabel_.empty()))
                    resolution = script_->root()->findPacketLabel(valueLabel_);

                script_->addVariable(name_, resolution);
            }
    };
}

NXMLElementReader* NXMLPDFReader::startContentSubElement(
        const std::string& subTagName, const regina::xml::XMLPropertyDict&) {
    if (subTagName == "pdf")
        return new NXMLCharsReader();
    else
        return new NXMLElementReader();
}

void NXMLPDFReader::endContentSubElement(const std::string& subTagName,
        NXMLElementReader* subReader) {
    if (subTagName == "pdf") {
        std::string base64 = dynamic_cast<NXMLCharsReader*>(subReader)->
            chars();

        // Strip out whitespace.
        std::string::iterator in = base64.begin();
        std::string::iterator out = base64.begin();
        while (in != base64.end()) {
            if (::isspace(*in))
                ++in;
            else {
                if (in == out) {
                    ++in;
                    ++out;
                } else
                    *out++ = *in++;
            }
        }

        // Is there any data at all?
        if (out == base64.begin()) {
            pdf->reset();
            return;
        }

        // Convert from base64.
        char* data;
        size_t dataLen;
        if (base64Decode(base64.c_str(), out - base64.begin(), &data, &dataLen))
            pdf->reset(data, dataLen, NPDF::OWN_NEW);
        else
            pdf->reset();
    }
}

NXMLElementReader* NXMLScriptReader::startContentSubElement(
        const std::string& subTagName,
        const regina::xml::XMLPropertyDict&) {
    if (subTagName == "text")
        return new NXMLCharsReader();
    else if (subTagName == "line") // Old-style
        return new NXMLCharsReader();
    else if (subTagName == "var")
        return new NScriptVarReader();
    else
        return new NXMLElementReader();
}

void NXMLScriptReader::endContentSubElement(const std::string& subTagName,
        NXMLElementReader* subReader) {
    if (subTagName == "text")
        script->setText(dynamic_cast<NXMLCharsReader*>(subReader)->chars());
    else if (subTagName == "line") { // Old-style
        script->append(dynamic_cast<NXMLCharsReader*>(subReader)->chars());
        script->append("\n");
    } else if (subTagName == "var") {
        NScriptVarReader* var = dynamic_cast<NScriptVarReader*>(subReader);
        if (! var->getName().empty())
            resolver_.queueTask(new VariableResolutionTask(
                script, var->getName(),
                var->getValueID(), var->getValueLabel()));
    }
}

NXMLPacketReader* NContainer::xmlReader(NPacket*,
        NXMLTreeResolver& resolver) {
    return new NXMLContainerReader(resolver);
}

NXMLPacketReader* NPDF::xmlReader(NPacket*, NXMLTreeResolver& resolver) {
    return new NXMLPDFReader(resolver);
}

NXMLPacketReader* NScript::xmlReader(NPacket*, NXMLTreeResolver& resolver) {
    return new NXMLScriptReader(resolver);
}

NXMLPacketReader* NText::xmlReader(NPacket*, NXMLTreeResolver& resolver) {
    return new NXMLTextReader(resolver);
}

} // namespace regina

