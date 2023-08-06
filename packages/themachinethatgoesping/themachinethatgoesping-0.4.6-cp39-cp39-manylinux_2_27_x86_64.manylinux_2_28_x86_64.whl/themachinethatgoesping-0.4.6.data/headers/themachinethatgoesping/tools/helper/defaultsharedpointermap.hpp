
// SPDX-FileCopyrightText: 2022 Peter Urban, Ghent University
//
// SPDX-License-Identifier: MPL-2.0
#include <map>
#include <memory>

namespace themachinethatgoesping {
namespace tools {
namespace helper {

template<typename t_key, typename t_value>
class DefaultSharedPointerMap : public std::map<t_key, std::shared_ptr<t_value>>
{
  public:
    // use all constructors of the base class
    DefaultSharedPointerMap() = default;

    std::shared_ptr<t_value>& at(const t_key& key)
    {
        auto it = this->find(key);

        if (it == this->end())
        {
            this->operator[](key) = std::make_shared<t_value>();

            return this->operator[](key);
        }
        return it->second;
    }

    std::shared_ptr<t_value> at_const(
        const t_key& key) const // TODO: this function is lying about constness. While the map is
                                // const, the return pointer and return value are not.
    {
        auto it = this->find(key);

        if (it == this->end())
        {
            return std::make_shared<t_value>();
        }
        return it->second;
    }
};

}
}
}