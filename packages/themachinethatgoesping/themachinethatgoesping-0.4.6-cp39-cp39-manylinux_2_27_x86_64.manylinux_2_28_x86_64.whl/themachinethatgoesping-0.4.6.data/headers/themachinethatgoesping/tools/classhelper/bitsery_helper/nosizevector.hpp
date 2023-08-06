// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0
//
// source: https://gitter.im/bitsery/Lobby Mindaugas Vinkelis @fraillt Oct 22 2021 13:10

// bitsery itself doesn't is lightweight, and doesnt include any unnessessary files,
// traits helps library to know how to use types correctly,
// in this case we'll be using vector both, to serialize/deserialize data and to store use as a
// buffer.
#include <bitsery/traits/vector.h>

namespace themachinethatgoesping {
namespace tools {
namespace bitsery_helper {

template<typename T>
class NoSizeVector
{
    // store size of container here, and pass it when creating an extension
    size_t _size;

    // serialize and deserialize function, as this flow is exactly the same for both
    template<typename SerDe, typename Fnc>
    void serDe(SerDe& serDe, T& obj, Fnc&& fnc) const
    {
        auto it    = obj.begin();
        auto endIt = it + _size;
        for (; it != endIt; ++it)
        {
            fnc(serDe, *it);
        }
    }

  public:
    explicit NoSizeVector(size_t size)
        : _size{ size }
    {
    }

    template<typename Ser, typename Fnc>
    void serialize(Ser& ser, const T& obj, Fnc&& fnc) const
    {
        serDe(ser, const_cast<T&>(obj), std::forward<Fnc>(fnc));
    }

    template<typename Des, typename Fnc>
    void deserialize(Des& des, T& obj, Fnc&& fnc) const
    {
        // resize obj, to make sure we don't override more than we need
        obj.resize(_size);
        serDe(des, obj, std::forward<Fnc>(fnc));
    }
};

}
}
}

template<typename T>
struct bitsery::traits::
    ExtensionTraits<themachinethatgoesping::tools::bitsery_helper::NoSizeVector<T>, T>
{
    // T is a container type, which has should have a value_type
    using TValue                                = typename T::value_type;
    static constexpr bool SupportValueOverload  = true;
    static constexpr bool SupportObjectOverload = true;
    static constexpr bool SupportLambdaOverload = true;
};