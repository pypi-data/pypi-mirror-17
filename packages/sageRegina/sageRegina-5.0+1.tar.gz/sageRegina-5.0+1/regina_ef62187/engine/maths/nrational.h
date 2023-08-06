
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

#ifndef __NRATIONAL_H
#ifndef __DOXYGEN
#define __NRATIONAL_H
#endif

/*! \file maths/nrational.h
 *  \brief Deals with artibrary precision rational numbers.
 */

#include "regina-core.h"
#include "maths/ninteger.h"

namespace regina {

/**
 * \weakgroup maths
 * @{
 */

/**
 * Represents an arbitrary precision rational number.
 * Calculations with NRational objects will be exact.
 *
 * Infinity (1/0) and undefined (0/0) are catered for.  (-1/0) is considered
 * the same as (1/0), and is represented as (1/0).
 * Any operation involving (0/0) will return (0/0).
 *
 * Since infinity is the same as negative infinity, both infinity plus
 * infinity and infinity minus infinity will return infinity.  Infinity
 * divided by infinity returns undefined, as does infinity times zero.
 *
 * For the purposes of ordering, undefined is the smallest rational and
 * infinity is the largest.  Undefined is always equal to itself, and
 * infinity is always equal to itself.
 *
 * When performing computations on rationals, the results will always be
 * stored in lowest terms (i.e., with relatively prime numerator and
 * denominator), and with a non-negative denominator.
 * However, when constructing a rational number from scratch (e.g., by
 * supplying the numerator and denominator separately), it is your
 * responsibility to ensure that the rational is in lowest terms.
 */
class REGINA_API NRational {
    public:
        static const NRational zero;
            /**< Globally available zero. */
        static const NRational one;
            /**< Globally available one. */
        static const NRational infinity;
            /**< Globally available infinity.  Note that both 1/0 and
             *   -1/0 evaluate to this same rational.  When queried,
             *   the representation 1/0 will be returned. */
        static const NRational undefined;
            /**< Globally available undefined.  This is represented as
             *   0/0. */
    private:
        /**
         * Represents the available flavours of rational number.
         */
        enum flavourType {
            f_infinity,
                /**< Infinity; there is only one rational of this type. */
            f_undefined,
                /**< Undefined; there is only one rational of this type. */
            f_normal
                /**< An ordinary rational (the denominator is non-zero). */
        };
        flavourType flavour;
            /**< Stores whether this rational is infinity, undefined or
             *   normal (non-zero denominator). */
        mpq_t data;
            /**< Contains the arbitrary precision rational data for normal
             *   (non-zero denominator) rationals.
             *   This is initialised even if the rational is infinite. */

        static const NRational maxDouble;
            /**< The largest positive rational number that can be converted
             *   to a finite double.  This begins as undefined, and is set
             *   to its correct value on the first call to doubleApprox(). */
        static const NRational minDouble;
            /**< The smallest positive rational number that can be converted
             *   to a non-zero double.  This begins as undefined, and is set
             *   to its correct value on the first call to doubleApprox(). */

    public:
        /**
         * Initialises to 0/1.
         */
        NRational();
        /**
         * Initialises to the given rational value.
         *
         * @param value the new rational value of this rational.
         */
        NRational(const NRational& value);
        /**
         * Initialises to the given integer value.
         * The given integer may be infinite.
         *
         * @param value the new integer value of this rational.
         */
        template <bool supportInfinity>
        NRational(const NIntegerBase<supportInfinity>& value);
        /**
         * Initialises to the given integer value.
         *
         * @param value the new integer value of this rational.
         */
        NRational(long value);
        /**
         * Initialises to <i>newNum</i>/<i>newDen</i>.
         *
         * \pre gcd(<i>newNum</i>, <i>newDen</i>) = 1 or <i>newDen</i> = 0.
         * \pre \a newDen is non-negative.
         *
         * \warning Failing to meet the preconditions above can result
         * in misleading or even undefined behaviour.  As an example,
         * NRational(4,4) (which breaks the gcd requirement) is
         * considered different from NRational(1,1) (a valid rational),
         * which is different again from NRational(-1,-1) (which breaks
         * the non-negativity requirement).
         *
         * \pre Neither of the given integers is infinite.
         *
         * @param newNum the new numerator.
         * @param newDen the new denominator.
         */
        template <bool supportInfinity>
        NRational(const NIntegerBase<supportInfinity>& newNum,
                  const NIntegerBase<supportInfinity>& newDen);
        /**
         * Initialises to <i>newNum</i>/<i>newDen</i>.
         *
         * \pre gcd(<i>newNum</i>, <i>newDen</i>) = 1 or <i>newDen</i> = 0.
         * \pre \a newDen is non-negative.
         *
         * \warning Failing to meet the preconditions above can result
         * in misleading or even undefined behaviour.  As an example,
         * NRational(4,4) (which breaks the gcd requirement) is
         * considered different from NRational(1,1) (a valid rational),
         * which is different again from NRational(-1,-1) (which breaks
         * the non-negativity requirement).
         *
         * @param newNum the new numerator.
         * @param newDen the new denominator.
         */
        NRational(long newNum, unsigned long newDen);
        /**
         * Destroys this rational.
         */
        ~NRational();

        /**
         * Sets this rational to the given rational value.
         *
         * @param value the new value of this rational.
         * @return a reference to this rational with its new value.
         */
        NRational& operator = (const NRational& value);
        /**
         * Sets this rational to the given integer value.
         * The given integer may be infinite.
         *
         * @param value the new value of this rational.
         * @return a reference to this rational with its new value.
         */
        template <bool supportInfinity>
        NRational& operator = (const NIntegerBase<supportInfinity>& value);
        /**
         * Sets this rational to the given integer value.
         *
         * @param value the new value of this rational.
         * @return a reference to this rational with its new value.
         */
        NRational& operator = (long value);
        /**
         * Swaps the values of this and the given rational.
         *
         * @param other the rational whose value will be swapped with
         * this.
         */
        void swap(NRational& other);

        /**
         * Returns the numerator of this rational.
         * Note that rationals are always stored in lowest terms with
         * non-negative denominator.  Infinity will be stored as 1/0.
         *
         * @return the numerator.
         */
        NInteger numerator() const;
        /**
         * Deprecated routine that returns the numerator of this rational.
         *
         * \deprecated This routine has been renamed to numerator().
         * See the numerator() documentation for further details.
         */
        REGINA_DEPRECATED NInteger getNumerator() const;
        /**
         * Returns the denominator of this rational.
         * Note that rationals are always stored in lowest terms with
         * non-negative denominator.  Infinity will be stored as 1/0.
         *
         * @return the denominator.
         */
        NInteger denominator() const;
        /**
         * Deprecated routine that returns the denominator of this rational.
         *
         * \deprecated This routine has been renamed to denominator().
         * See the denominator() documentation for further details.
         */
        REGINA_DEPRECATED NInteger getDenominator() const;

        /**
         * Calculates the product of two rationals.
         * This rational is not changed.
         *
         * @param r the rational with which to multiply this.
         * @return the product \a this * \a r.
         */
        NRational operator *(const NRational& r) const;
        /**
         * Calculates the ratio of two rationals.
         * This rational is not changed.
         *
         * @param r the rational to divide this by.
         * @return the ratio \a this / \a r.
         */
        NRational operator /(const NRational& r) const;
        /**
         * Calculates the sum of two rationals.
         * This rational is not changed.
         *
         * @param r the rational to add to this.
         * @return the sum \a this + \a r.
         */
        NRational operator +(const NRational& r) const;
        /**
         * Calculates the difference of two rationals.
         * This rational is not changed.
         *
         * @param r the rational to subtract from this.
         * @return the difference \a this - \a r.
         */
        NRational operator -(const NRational& r) const;
        /**
         * Determines the negative of this rational.
         * This rational is not changed.
         *
         * @return the negative of this rational.
         */
        NRational operator - () const;
        /**
         * Calculates the inverse of this rational.
         * This rational is not changed.
         *
         * @return the inverse 1 / \a this.
         */
        NRational inverse() const;
        /**
         * Determines the absolute value of this rational.
         * This rational is not changed.
         *
         * @return the absolute value of this rational.
         */
        NRational abs() const;

        /**
         * Adds the given rational to this.
         * This rational is changed to reflect the result.
         *
         * @param other the rational to add to this.
         * @return a reference to this rational with its new value.
         */
        NRational& operator += (const NRational& other);
        /**
         * Subtracts the given rational from this.
         * This rational is changed to reflect the result.
         *
         * @param other the rational to subtract from this.
         * @return a reference to this rational with its new value.
         */
        NRational& operator -= (const NRational& other);
        /**
         * Multiplies the given rational by this.
         * This rational is changed to reflect the result.
         *
         * @param other the rational to multiply by this.
         * @return a reference to this rational with its new value.
         */
        NRational& operator *= (const NRational& other);
        /**
         * Divides this by the given rational.
         * This rational is changed to reflect the result.
         *
         * @param other the rational to divide this by.
         * @return a reference to this rational with its new value.
         */
        NRational& operator /= (const NRational& other);
        /**
         * Negates this rational.
         * This rational is changed to reflect the result.
         */
        void negate();
        /**
         * Inverts this rational.
         * This rational is changed to reflect the result.
         */
        void invert();

        /**
         * Determines if this is equal to the given rational.
         *
         * @param compare the rational with which this will be compared.
         * @return \c true if and only if this rational is equal to
         * \a compare.
         */
        bool operator == (const NRational& compare) const;
        /**
         * Determines if this is not equal to the given rational.
         *
         * @param compare the rational with which this will be compared.
         * @return \c true if and only if this rational is not equal to
         * \a compare.
         */
        bool operator != (const NRational& compare) const;
        /**
         * Determines if this is less than the given rational.
         *
         * @param compare the rational with which this will be compared.
         * @return \c true if and only if this rational is less than
         * \a compare.
         */
        bool operator < (const NRational& compare) const;
        /**
         * Determines if this is greater than the given rational.
         *
         * @param compare the rational with which this will be compared.
         * @return \c true if and only if this rational is greater than
         * \a compare.
         */
        bool operator > (const NRational& compare) const;
        /**
         * Determines if this is less than or equal to the given rational.
         *
         * @param compare the rational with which this will be compared.
         * @return \c true if and only if this rational is less than or
         * equal to \a compare.
         */
        bool operator <= (const NRational& compare) const;
        /**
         * Determines if this is greater than or equal to the given rational.
         *
         * @param compare the rational with which this will be compared.
         * @return \c true if and only if this rational is greater than
         * or equal to \a compare.
         */
        bool operator >= (const NRational& compare) const;

        /**
         * Attempts to convert this rational to a real number.
         *
         * If this rational can be approximated by a double
         * (specifically, if it lies within double's allowable range)
         * then a such an approximation is returned.  Otherwise zero is
         * returned instead.
         *
         * The optional \a inRange argument allows the result of range
         * checking to be returned explicitly as a boolean
         * (<tt>*inRange</tt> will be set to \c true if a double
         * approximation is possible and \c false otherwise).
         *
         * It is safe to pass \a inRange as \c null, in which case this
         * boolean is not returned.  Range checking is still performed
         * internally however, i.e., zero is still returned if the rational
         * is out of range.
         *
         * Note that "lies with double's allowable range" is
         * machine-dependent, and may vary between different installations.
         * Infinity and undefined are always considered out of range.
         * Otherwise a rational is out of range if its absolute value is
         * finite but too large (e.g., 10^10000) or non-zero but too small
         * (e.g., 10^-10000).
         *
         * @param inRange returns the result of range checking as
         * described above; this pointer may be passed as \c null if
         * the caller does not care about this result.
         * @return the double approximation to this rational, or zero if
         * this rational lies outside double's allowable range.
         *
         * \ifacespython The \a inRange argument is not present.
         * Instead there are two versions of this routine.
         * The first is \a doubleApprox(), which returns a single real
         * number.  The second is \a doubleApproxCheck(), which returns
         * a (real, bool) pair containing the converted real number
         * followed by the result of range checking.
         *
         * @author Ryan Budney, B.B.
         */
        double doubleApprox(bool* inRange = 0) const;

        /**
         * Returns this rational as written using TeX formatting.
         * No leading or trailing dollar signs will be included.
         *
         * @return this rational as written using TeX formatting.
         *
         * @author Ryan Budney
         */
        std::string TeX() const;
        /**
         * Deprecated routine that returns this rational as written using TeX
         * formatting.
         *
         * \deprecated This routine has been renamed to TeX().
         * See the TeX() documentation for further details.
         */
        REGINA_DEPRECATED std::string getTeX() const;

        /**
         * Writes this rational in TeX format to the given output stream.
         * No leading or trailing dollar signs will be included.
         *
         * \ifacespython The parameter \a out does not exist; instead
         * standard output will always be used.  Moreover, this routine
         * returns \c None.
         *
         * @param out the output stream to which to write.
         * @return a reference to the given output stream.
         *
         * @author Ryan Budney
         */
        std::ostream& writeTeX(std::ostream& out) const;

    private:
        /**
         * Initialises the class constants \a maxDouble and \a minDouble.
         * These constants are used by doubleApprox(), and so this routine
         * is called the first time that doubleApprox() is run.
         */
        static void initDoubleBounds();

    friend std::ostream& operator << (std::ostream& out, const NRational& rat);
};

/**
 * Writes the given rational to the given output stream.
 * Infinity will be written as <tt>Inf</tt>.  Undefined will be written
 * as <tt>Undef</tt>.  A rational with denominator one will be written
 * as a single integer.  All other rationals will be written in the form
 * <tt>r/s</tt>.
 *
 * @param out the output stream to which to write.
 * @param rat the rational to write.
 * @return a reference to \a out.
 */
REGINA_API std::ostream& operator << (std::ostream& out, const NRational& rat);

/*@}*/

// Inline functions for NRational

inline NRational::NRational() : flavour(f_normal) {
    mpq_init(data);
}
inline NRational::NRational(const NRational& value) : flavour(value.flavour) {
    mpq_init(data);
    if (flavour == f_normal)
        mpq_set(data, value.data);
}
template <bool supportInfinity>
inline NRational::NRational(const NIntegerBase<supportInfinity>& value) :
        flavour(f_normal) {
    mpq_init(data);
    if (value.isInfinite())
        flavour = f_infinity;
    else if (value.isNative())
        mpq_set_si(data, value.longValue(), 1);
    else
        mpq_set_z(data, value.rawData());
}
inline NRational::NRational(long value) : flavour(f_normal) {
    mpq_init(data);
    mpq_set_si(data, value, 1);
}
template <bool supportInfinity>
NRational::NRational(const NIntegerBase<supportInfinity>& newNum,
                     const NIntegerBase<supportInfinity>& newDen) {
    mpq_init(data);
    if (newDen.isZero()) {
        if (newNum.isZero())
            flavour = f_undefined;
        else
            flavour = f_infinity;
    } else {
        flavour = f_normal;
        if (newNum.isNative() && newDen.isNative())
            mpq_set_si(data, newNum.longValue(), newDen.longValue());
        else if (newNum.isNative()) {
            // Avoid bloating newNum with a GMP representation.
            NIntegerBase<supportInfinity> tmp(newNum);
            mpz_set(mpq_numref(data), tmp.rawData());
            mpz_set(mpq_denref(data), newDen.rawData());
        } else if (newDen.isNative()) {
            // Avoid bloating newDen with a GMP representation.
            NIntegerBase<supportInfinity> tmp(newDen);
            mpz_set(mpq_numref(data), newNum.rawData());
            mpz_set(mpq_denref(data), tmp.rawData());
        } else {
            mpz_set(mpq_numref(data), newNum.rawData());
            mpz_set(mpq_denref(data), newDen.rawData());
        }
    }
}
inline NRational::~NRational() {
    mpq_clear(data);
}

inline NRational& NRational::operator = (const NRational& value) {
    flavour = value.flavour;
    if (flavour == f_normal)
        mpq_set(data, value.data);
    return *this;
}
template <bool supportInfinity>
inline NRational& NRational::operator = (
        const NIntegerBase<supportInfinity>& value) {
    if (value.isInfinite())
        flavour = f_infinity;
    else if (value.isNative()) {
        flavour = f_normal;
        mpq_set_si(data, value.longValue(), 1);
    } else {
        flavour = f_normal;
        mpq_set_z(data, value.rawData());
    }
    return *this;
}
inline NRational& NRational::operator = (long value) {
    flavour = f_normal;
    mpq_set_si(data, value, 1);
    return *this;
}

inline void NRational::swap(NRational& other) {
    std::swap(flavour, other.flavour);
    mpq_swap(data, other.data);
}

inline void NRational::negate() {
    if (flavour == f_normal)
        mpq_neg(data, data);
}

inline NInteger NRational::getNumerator() const {
    return numerator();
}

inline NInteger NRational::getDenominator() const {
    return denominator();
}

inline std::string NRational::getTeX() const {
    return TeX();
}

inline bool NRational::operator <= (const NRational& compare) const {
    return ! (*this > compare);
}
inline bool NRational::operator >= (const NRational& compare) const {
    return ! (*this < compare);
}
inline bool NRational::operator != (const NRational& compare) const {
    return ! (*this == compare);
}

} // namespace regina

#endif
