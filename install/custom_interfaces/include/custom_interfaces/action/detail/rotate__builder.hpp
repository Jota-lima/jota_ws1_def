// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:action/Rotate.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__ACTION__DETAIL__ROTATE__BUILDER_HPP_
#define CUSTOM_INTERFACES__ACTION__DETAIL__ROTATE__BUILDER_HPP_

#include "custom_interfaces/action/detail/rotate__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_Goal_angle_degrees
{
public:
  Init_Rotate_Goal_angle_degrees()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::action::Rotate_Goal angle_degrees(::custom_interfaces::action::Rotate_Goal::_angle_degrees_type arg)
  {
    msg_.angle_degrees = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_Goal>()
{
  return custom_interfaces::action::builder::Init_Rotate_Goal_angle_degrees();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_Result_final_angle
{
public:
  explicit Init_Rotate_Result_final_angle(::custom_interfaces::action::Rotate_Result & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::action::Rotate_Result final_angle(::custom_interfaces::action::Rotate_Result::_final_angle_type arg)
  {
    msg_.final_angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_Result msg_;
};

class Init_Rotate_Result_success
{
public:
  Init_Rotate_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Rotate_Result_final_angle success(::custom_interfaces::action::Rotate_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Rotate_Result_final_angle(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_Result>()
{
  return custom_interfaces::action::builder::Init_Rotate_Result_success();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_Feedback_remaining_degrees
{
public:
  Init_Rotate_Feedback_remaining_degrees()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::action::Rotate_Feedback remaining_degrees(::custom_interfaces::action::Rotate_Feedback::_remaining_degrees_type arg)
  {
    msg_.remaining_degrees = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_Feedback>()
{
  return custom_interfaces::action::builder::Init_Rotate_Feedback_remaining_degrees();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_SendGoal_Request_goal
{
public:
  explicit Init_Rotate_SendGoal_Request_goal(::custom_interfaces::action::Rotate_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::action::Rotate_SendGoal_Request goal(::custom_interfaces::action::Rotate_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_SendGoal_Request msg_;
};

class Init_Rotate_SendGoal_Request_goal_id
{
public:
  Init_Rotate_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Rotate_SendGoal_Request_goal goal_id(::custom_interfaces::action::Rotate_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Rotate_SendGoal_Request_goal(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_SendGoal_Request>()
{
  return custom_interfaces::action::builder::Init_Rotate_SendGoal_Request_goal_id();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_SendGoal_Response_stamp
{
public:
  explicit Init_Rotate_SendGoal_Response_stamp(::custom_interfaces::action::Rotate_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::action::Rotate_SendGoal_Response stamp(::custom_interfaces::action::Rotate_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_SendGoal_Response msg_;
};

class Init_Rotate_SendGoal_Response_accepted
{
public:
  Init_Rotate_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Rotate_SendGoal_Response_stamp accepted(::custom_interfaces::action::Rotate_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Rotate_SendGoal_Response_stamp(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_SendGoal_Response>()
{
  return custom_interfaces::action::builder::Init_Rotate_SendGoal_Response_accepted();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_GetResult_Request_goal_id
{
public:
  Init_Rotate_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::action::Rotate_GetResult_Request goal_id(::custom_interfaces::action::Rotate_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_GetResult_Request>()
{
  return custom_interfaces::action::builder::Init_Rotate_GetResult_Request_goal_id();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_GetResult_Response_result
{
public:
  explicit Init_Rotate_GetResult_Response_result(::custom_interfaces::action::Rotate_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::action::Rotate_GetResult_Response result(::custom_interfaces::action::Rotate_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_GetResult_Response msg_;
};

class Init_Rotate_GetResult_Response_status
{
public:
  Init_Rotate_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Rotate_GetResult_Response_result status(::custom_interfaces::action::Rotate_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Rotate_GetResult_Response_result(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_GetResult_Response>()
{
  return custom_interfaces::action::builder::Init_Rotate_GetResult_Response_status();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace action
{

namespace builder
{

class Init_Rotate_FeedbackMessage_feedback
{
public:
  explicit Init_Rotate_FeedbackMessage_feedback(::custom_interfaces::action::Rotate_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::action::Rotate_FeedbackMessage feedback(::custom_interfaces::action::Rotate_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_FeedbackMessage msg_;
};

class Init_Rotate_FeedbackMessage_goal_id
{
public:
  Init_Rotate_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Rotate_FeedbackMessage_feedback goal_id(::custom_interfaces::action::Rotate_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Rotate_FeedbackMessage_feedback(msg_);
  }

private:
  ::custom_interfaces::action::Rotate_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::action::Rotate_FeedbackMessage>()
{
  return custom_interfaces::action::builder::Init_Rotate_FeedbackMessage_goal_id();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__ACTION__DETAIL__ROTATE__BUILDER_HPP_
